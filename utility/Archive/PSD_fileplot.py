import scipy.signal as sig
import librosa
import matplotlib.pyplot as plt

def PSD_fileplot(file_path,
                 PSD_window='hamming',
                 PSD_nperseg = 128,
                 PSD_nfft=512,
                 PSD_scaling='spectrum',
                 ChannelNr=[0],
                 color='blue'):

    audio_ch, sr = librosa.load(file_path, sr=None, mono=False)
    for ch in ChannelNr:
        f, Pxx = sig.welch(audio_ch[ch],sr,
                       window=PSD_window,
                       nperseg=PSD_nperseg, 
                       noverlap=False, 
                       nfft=PSD_nfft,
                       scaling=PSD_scaling)


        plt.plot(f, Pxx, color=color)
        ax = plt.gca()
        ax.set_xscale('log')
        ax.set_yscale('log')