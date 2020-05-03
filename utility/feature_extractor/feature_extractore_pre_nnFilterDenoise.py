print('load feature_extractore_pre_nnFilterDenoise')


class feature_extractor_pre_nnFilterDenoise(feature_extractor):
    def __init__(self, base_folder, name='nnfilt'):
        super().__init__(base_folder,name,
                        xlabel = 'time',
                        ylabel = 'amp',
                        zlabel = 'none')
        
        
        # set type
        self.para_dict['type'] = feature_extractor_type.preNNFILTER
        self.para_dict['type_name'] = 'pNNfilt'
        # default hyper
        self.set_hyperparamter()


    def set_hyperparamter(self,
                           aggregation=np.average,
                           nfft=2048, 
                           channel = 'all'):

        self.para_dict['hyperpara']={ \
                'aggregation': aggregation,
                'nfft': nfft,
                'channel': channel}
        
        #self.para_dict['file_name_mainhyperparastr'] = 'nf'+str(nfft)

        if os.path.isfile(self._full_wave_path()):
                self.create_from_wav(self.para_dict['wave_filepath'] )
        
    def create_from_wav(self, filepath):

        # assuming for now all channels
        self.para_dict['data_channel_use_str'] = 'ch'+'All'
        af = np.array(self._read_wav(filepath))

        # mod here   
        # make list of spectra not of time doamin
        # make list dependent
        if self.para_dict['hyperpara']['channel']=='all':
            cl = range(af.shape[0])
        elif type(self.para_dict['hyperpara']['channel'])==int:
            cl = [self.para_dict['hyperpara']['channel']]
        elif type(self.para_dict['hyperpara']['channel'])==list:
            cl = self.para_dict['hyperpara']['channel']
            
        for c in cl:
            # Stft
            S = np.abs(librosa.stft(af[c,:],n_fft=self.para_dict['hyperpara']['nfft']))
            nlm = librosa.decompose.nn_filter(S,aggregate=self.para_dict['hyperpara']['aggregation'], axis=1)
            den = librosa.core.istft(nlm)
            af[c,:len(den)] = librosa.core.istft(nlm)
            af[c,len(den):]=0.

            
        self.feature_data = af
    
    def get_wav_memory_file(self):
        # move taransforamtion to time here
        wmf = feature_extractor_memory_wave_file()
        wmf.filepath = self.para_dict['wave_filepath']
        wmf.channel = self.feature_data
        wmf.srate= self.para_dict['wave_srate']
        wmf.length = self.feature_data.shape[1] # TODO if one dim
        return wmf

    def get_fft_memory_file(self):
        # return sfft per channel
        stftf = 1
        return stftf 


    
