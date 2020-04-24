print('load feature_extractor_psd')

# TODO: concat all channels 
# TODO: matrix over all channels

class feature_extractor_welchPSD(feature_extractor):
    def __init__(self, base_folder, name='mel_spectra'):
        super().__init__(base_folder,name,
                        xlabel = 'freq',
                        ylabel = 'V**2',
                        zlabel = 'none')
        
        # set type
        self.para_dict['type'] = feature_extractor_type.WELECHPSD
        
        # default hyper
        self.set_hyperparamter()

    def set_hyperparamter(self,
                              window='hamming', 
                              nfft=512,
                              nperseg =128,
                              scaleing='spectrum'):
            
            self.para_dict['hyperpara']={ \
            'window': window,
            'nfft': nfft,
            'nperseg': nperseg,
            'scaleing': scaleing}
            

            
            if os.path.isfile(self._full_wave_path()):
                self.create_from_wav(self.para_dict['wave_filepath'], channel=self.para_dict['wave_channel'][0] )
                
    def create_from_wav(self, filepath, channel=0, multichannel='concat'):
        # multichannel = 'concat', 'stack_matrix'
        # channel= int single channel else list or str 'all'
        
        # TODO for the multichannel stuff... if int or list
        self.para_dict['wave_channel'] = [channel]
        af = np.array(self._read_wav(filepath))[channel, :]
        f, Pxx = scipy.signal.welch(af,
                           fs=self.para_dict['wave_srate'],
                           window=self.para_dict['hyperpara']['window'],
                           nperseg=self.para_dict['hyperpara']['nperseg'], 
                           noverlap=False, 
                           nfft=self.para_dict['hyperpara']['nfft'],
                           scaling=self.para_dict['hyperpara']['scaleing'])
        
        self.feature_data = {'f': f, 'Pxx': Pxx}
     
    def plot(self, loglog=True):
        plt.plot(self.feature_data['f'],self.feature_data['Pxx'])
        plt.xlabel(self.para_dict['xlabel'])
        plt.ylabel(self.para_dict['ylabel'])
        if loglog:
            plt.xscale('log')
            plt.yscale('log')
            plt.ylabel('log(' + self.para_dict['ylabel'] +')')
        else:
            plt.xscale('log')
        plt.title(f"welch {self.para_dict['hyperpara']['scaleing']} - {self.name}")
     
    def flat_feature(self):
        return self.feature_data['Pxx']
     
    def freq_axis(self):
        return self.feature_data['f']
        