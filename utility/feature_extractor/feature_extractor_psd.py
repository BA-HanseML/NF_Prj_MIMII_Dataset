print('load feature_extractor_psd')

# TODO: concat all channels 
# TODO: matrix over all channels

class feature_extractor_welchPSD(feature_extractor):
    def __init__(self, base_folder, name='welch'):
        super().__init__(base_folder,name,
                        xlabel = 'freq',
                        ylabel = 'V**2',
                        zlabel = 'none')
        
        self.stack = False
        # set type
        self.para_dict['type'] = feature_extractor_type.WELECHPSD
        self.para_dict['type_name'] = 'welchPSD'
        # default hyper
        self.set_hyperparamter()

    def set_hyperparamter(self,
                              window='hamming', 
                              nfft=512,
                              nperseg =128,
                              scaleing='spectrum',
                              multichannel='none',
                              channel=0):
            
            self.para_dict['hyperpara']={ \
            'window': window,
            'nfft': nfft,
            'nperseg': nperseg,
            'scaleing': scaleing,
            'multichannel': multichannel,
            'channel': channel}
            
            self.para_dict['file_name_mainhyperparastr'] = 'seg'+str(nperseg)
            
            if os.path.isfile(self._full_wave_path()):
                self.create_from_wav(self.para_dict['wave_filepath'] )
                
    def create_from_wav(self, filepath):
        # multichannel = 'concat', 'stack_matrix'
        # channel= int single channel else list or str 'all'
        
        # TODO for the multichannel stuff... if int or list
        channel = self.para_dict['hyperpara']['channel']
        multichannel = self.para_dict['hyperpara']['multichannel']
        self.stack = False
        if  multichannel=='concat' and channel=='all':
            self.para_dict['data_channel_use_str'] = 'ch'+'Allc'
            af = np.array(self._read_wav(filepath))
            self.para_dict['wave_channel'] = [c+1 for c in range(af.shape[0])]
            af= af.flatten()
        elif multichannel=='stack' and channel=='all':
            af = np.array(self._read_wav(filepath))
            self.para_dict['data_channel_use_str'] = 'ch'+'Allc'
            self.para_dict['wave_channel'] = [c+1 for c in range(af.shape[0])]
            self.stack = True
        else:
            self.para_dict['data_channel_use_str'] = 'ch'+str(channel)
            self.para_dict['wave_channel'] = [channel]
            af = np.array(self._read_wav(filepath))[channel, :]
        
        
        
        
        if not self.stack:
            f, Pxx = scipy.signal.welch(af,
                           fs=self.para_dict['wave_srate'],
                           window=self.para_dict['hyperpara']['window'],
                           nperseg=self.para_dict['hyperpara']['nperseg'], 
                           noverlap=False, 
                           nfft=self.para_dict['hyperpara']['nfft'],
                           scaling=self.para_dict['hyperpara']['scaleing'])
        else: #  stacking
            
            for c in range(af.shape[0]):
                f, Pc = scipy.signal.welch(af[c],
                           fs=self.para_dict['wave_srate'],
                           window=self.para_dict['hyperpara']['window'],
                           nperseg=self.para_dict['hyperpara']['nperseg'], 
                           noverlap=False, 
                           nfft=self.para_dict['hyperpara']['nfft'],
                           scaling=self.para_dict['hyperpara']['scaleing'])
                if c == 0:
                    Pxx = Pc
                else:
                    Pxx = np.vstack((Pc,Pxx))

                           
        
        self.feature_data = {'f': f, 'Pxx': Pxx}
     
    def plot(self, loglog=True):
        if not self.stack:
            plt.plot(self.feature_data['f'],self.feature_data['Pxx'], 
            label = self.para_dict['wave_filepath'])
        else:
            for c in range(len(self.feature_data['Pxx'][:,0])):
                plt.plot(self.feature_data['f'],self.feature_data['Pxx'][c], label='ch'+str(c))

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
        