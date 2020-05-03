# Created by Teng Xiang at 2018-08-10
# Current version: 2018-08-10 
# https://github.com/helianvine/fdndlp
# =============================================================================

""" Weighted prediction error(WPE) method for speech dereverberation."""

#import stft
import argparse
import time
import os
import numpy as np
#import soundfile as sf
import librosa
from numpy.lib import stride_tricks
# import matplotlib.pyplot as plt


import numpy as np
from numpy.lib import stride_tricks

def wpe_stft(data, frame_size=512, overlap=0.75, window=None):
    """ Multi-channel short time fourier transform 

    Args:
        data: A 2-dimension numpy array with shape=(channels, samples)
        frame_size: An integer number of the length of the frame
        overlap: A float nonnegative number less than 1 indicating the overlap
                 factor between adjacent frames

    Return:
        A 3-dimension numpy array with shape=(channels, frames, frequency_bins) 
    """
    assert(data.ndim == 2)
    if window == None:
        window = np.hanning(frame_size) 
    frame_shift = int(frame_size - np.floor(overlap * frame_size))
    cols = int(np.ceil((data.shape[1] - frame_size) / frame_shift)) + 1
    data = np.concatenate(
        (data, np.zeros((data.shape[0], frame_shift), dtype = np.float32)),
        axis = 1)
    samples = data.copy()
    frames = stride_tricks.as_strided(
        samples,
        shape=(samples.shape[0], cols, frame_size),
        strides=(
            samples.strides[-2], 
            samples.strides[-1] * frame_shift, 
            samples.strides[-1])).copy()
    frames *= window
    return np.fft.rfft(frames)

def wpe_istft(data, frame_size=None, overlap=0.75, window=None):
    """ Multi-channel inverse short time fourier transform

    Args:
        data: A 3-dimension numpy array with shape=(channels, frames, frequency_bins) 
        frame_size: An integer number of the length of the frame
        overlap: A float nonnegative number less than 1 indicating the overlap
                 factor between adjacent frames

    Return:
        A 2-dimension numpy array with shape=(channels, samples)
    """
    assert(data.ndim == 3)
    real_data = np.fft.irfft(data)
    if frame_size == None:
        frame_size = real_data.shape[-1]
    frame_num = data.shape[-2]
    frame_shift = int(frame_size - np.floor(frame_size * overlap))
    length = (frame_num - 1) * frame_shift + frame_size
    output = np.zeros((data.shape[0], length))
    for i in range(frame_num):
        index = i*frame_shift
        output[:, index : index + frame_size] += real_data[:,i]
    return output
    
def wpe_log_spectrum(raw_data, frame_length=512):
    """Log magnitude spectrogram"""
    if raw_data.ndim == 1:
        raw_data = np.reshape(raw_data, (1, -1))
    freq_data = wpe_stft(raw_data)
    phase = np.angle(freq_data)
    freq_data = np.abs(freq_data)
    freq_data = np.maximum(freq_data, 1e-8)
    log_data = np.log10(freq_data / freq_data.min())
    return log_data, phase



class WpeMethod(object):
    """WPE metheod for speech dereverberaiton 

    Weighted prediction errors (WPE) method is an outstanding speech 
    derverberation algorithm, which is based on the multi-channel linear
    prediction algorithm and produces multi-channel output.

    Attributes:
        channels: Number of input channels.
        out_num: Number of output channels.
        p: An integer number of the prediction order.
        d: An integer number of the prediction delay.
        frame_size: An integer number of the length of the frame
        overlap: A float nonnegative number less than 1 indicating the overlap
                 factor between adjacent frames
    """
    def __init__(self, mic_num, out_num, order=30 , verbose=False):
        self.channels = mic_num
        self.out_num = out_num
        self.p = order
        self.d = 2
        self.frame_size = 512
        self.overlap = 0.5
        self._iterations = 2
        self.verbose = verbose
    
    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        assert(int(value) > 0)
        self._iterations = int(value)

    def _display_cfgs(self):
        if self.verbose:
            print('\nSettings:')
            print("Input channel: %d" % self.channels)
            print("Output channel: %d" % self.out_num)
            print("Prediction order: %d\n" % self.p)


    def run_offline(self, data):
        self._display_cfgs()
        time_start = time.time()
        if self.verbose:
            print("Processing...")
        drv_data = self.__fdndlp(data)
        if self.verbose:
            print("Done!\nTotal time: %f\n" % (time.time() - time_start))
        return drv_data

    def __fdndlp(self, data):
        """Frequency-domain variance-normalized delayed liner prediction 

        This is the core part of the WPE method. The variance-normalized 
        linear prediciton algorithm is implemented in each frequency bin 
        separately. Both the input and output signals are in time-domain.  

        Args:
            data: A 2-dimension numpy array with shape=(chanels, samples)

        Returns:
            A 2-dimension numpy array with shape=(output_channels, samples)
        """

        freq_data = wpe_stft(
            data / np.abs(data).max(), 
            frame_size=self.frame_size, overlap=self.overlap)
        self.freq_num = freq_data.shape[-1]
        drv_freq_data = freq_data[0:self.out_num].copy()
        for i in range(self.freq_num):
            xk = freq_data[:,:,i].T
            dk = self.__ndlp(xk)
            drv_freq_data[:,:,i] = dk.T
        drv_data = wpe_istft(
            drv_freq_data, 
            frame_size=self.frame_size, overlap=self.overlap)
        return drv_data / np.abs(drv_data).max()


    def __ndlp(self, xk):
        """Variance-normalized delayed liner prediction 

        Here is the specific WPE algorithm implementation. The input should be
        the reverberant time-frequency signal in a single frequency bin and 
        the output will be the dereverberated signal in the corresponding 
        frequency bin.

        Args:
            xk: A 2-dimension numpy array with shape=(frames, input_chanels)

        Returns:
            A 2-dimension numpy array with shape=(frames, output_channels)
        """
        cols = xk.shape[0] - self.d
        xk_buf = xk[:,0:self.out_num]
        xk = np.concatenate(
            (np.zeros((self.p - 1, self.channels)), xk),
            axis=0)
        xk_tmp = xk[:,::-1].copy()
        frames = stride_tricks.as_strided(
            xk_tmp,
            shape=(self.channels * self.p, cols),
            strides=(xk_tmp.strides[-1], xk_tmp.strides[-1]*self.channels))
        frames = frames[::-1]
        sigma2 = np.mean(1 / (np.abs(xk_buf[self.d:]) ** 2), axis=1)
        for _ in range(self.iterations):
            x_cor_m = np.dot(
                    np.dot(frames, np.diag(sigma2)),
                    np.conj(frames.T))
            x_cor_v = np.dot(
                frames, 
                np.conj(xk_buf[self.d:] * sigma2.reshape(-1, 1)))
            coeffs = np.dot(np.linalg.inv(x_cor_m), x_cor_v)
            dk = xk_buf[self.d:] - np.dot(frames.T, np.conj(coeffs))
            sigma2 = np.mean(1 / (np.abs(dk) ** 2), axis=1)
        return np.concatenate((xk_buf[0:self.d], dk))

    def load_audio(self, filename):
        #data, fs = sf.read(filename, always_2d=True)
        data, fs = librosa.load(filename,  sr=None, mono=False)
        #data = data.T
        assert(data.shape[0] >= self.channels)
        if data.shape[0] > self.channels:
            print(
                "The number of the input channels is %d," % data.shape[0],
                "and only the first %d channels are loaded." % self.channels)
            data = data[0: self.channels]
        return data.copy(), fs

    def write_wav(self, data, fs, filename, path='wav_out'):
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        print('Write to file: %s.' % filepath)
        sf.write(filepath, data.T, fs, subtype='PCM_16')


