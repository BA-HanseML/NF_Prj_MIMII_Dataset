print('load feature_extractor_mel_spectra')

# Feature extractor for handling MEL spectra

class feature_extractor_mel(feature_extractor):
    def __init__(self, base_folder, name='mel_spectra'):
        super().__init__(base_folder,name,
                        xlabel = 'time',
                        ylabel = 'freq',
                        zlabel = 'log mel energy')
        
        # set type
        self.para_dict['type'] = feature_extractor_type.MEL_SPECTRUM
        self.para_dict['type_name'] = 'MEL'
        
        # default hyper
        self.set_hyperparamter()

    def set_hyperparamter(self,
                              n_mels=64, 
                              n_fft=1024,
                              power=2.0,
                              hop_length=512,
                              channel=0):
            
            self.para_dict['hyperpara']={ \
            'n_mels': n_mels,
            'n_fft': n_fft,
            'power': power,
            'hop_length': hop_length,
            'channel': channel}
            
            self.para_dict['file_name_mainhyperparastr'] = 'nm'+str(n_mels) 
            
            if os.path.isfile(self._full_wave_path()):
                #print('recalc mel')
                self.create_from_wav(self.para_dict['wave_filepath'] )
            
            
    def create_from_wav(self, filepath):

            # calc librosa 

            channel = self.para_dict['hyperpara']['channel']
            #multichannel = self.para_dict['hyperpara']['multichannel']
            self.para_dict['data_channel_use_str'] = 'ch'+str(channel)
            
            self.para_dict['wave_channel'] = [channel]
            af = np.array(self._read_wav(filepath))[channel, :]
            power=self.para_dict['hyperpara']['power']
            
            mel_spectrogram = librosa.feature.melspectrogram(y=af, \
            sr=self.para_dict['wave_srate'],
            n_fft=self.para_dict['hyperpara']['n_fft'],
            hop_length=self.para_dict['hyperpara']['hop_length'],
            n_mels=self.para_dict['hyperpara']['n_mels'],
            power=power)
            
            log_mel_spectrogram = 20.0 / power * np.log10(mel_spectrogram + sys.float_info.epsilon)
            
            self.feature_data = log_mel_spectrogram
            
    def plot(self, colorbar=True):
            librosa.display.specshow(self.feature_data,
            x_axis='time',
            y_axis='mel',
            sr=self.para_dict['wave_srate']) #time_fmt ='ms' # time format not rubust
            plt.title('Mel Spectrum ' + self.para_dict['wave_filepath'])
            if colorbar:
                plt.colorbar(format='%+2.0f dB')
     
    def flat_feature(self):
        return self.feature_data.flatten()
        pass
    
    def freq_axis(self):
        return np.linspace(0,self.para_dict['wave_srate']/2, self.para_dict['hyperpara']['n_mels'])
    
    def time_axis(self):
        return np.linspace(0,self.para_dict['wave_length']/self.para_dict['wave_srate'],len(self.feature_data[:,0]))

    def frame_pack_feature(self, frames):
        vectorarray_size = len(self.feature_data[0, :]) - frames + 1
        n_mels = self.feature_data.shape[0]

        vectorarray = np.zeros((vectorarray_size, n_mels * frames), float)
        for t in range(frames):
            vectorarray[:, n_mels * t: n_mels * (t + 1)] = self.feature_data[:, t: t + vectorarray_size].T
        
        return vectorarray

    def get_feature(self, feat_para_dict):
        if feat_para_dict['function'] == 'flat':
            return self.flat_feature()
        elif feat_para_dict['function'] == 'frame':
            return self.frame_pack_feature( feat_para_dict['frames'])
        else:
             raise Exception('feat get function "' + feat_para_dict['function'] + '" unknown')

        