print('load # extractor diagram V0 all channel to psd')

class extdia_v0_allch(extractor_diagram):

    def ini_diagram(self): # custom
    
        # extractor diagram name
        self.name = 'EDiaV0'
        
        # extractor pre objects 
        self.pre['denoise'] = feature_extractor_pre_nnFilterDenoise(self.base_folder,'den')
        self.pre['denoise'].set_hyperparamter(aggregation=np.mean, channel='all')
        
        # extractor objects
        self.ext['MEL_den'] = feature_extractor_mel(self.base_folder,'MEL_den')
        self.ext['MEL_den'].set_hyperparamter(n_fft=1024, n_mels=80, hop_length=512,  channel=0)
        
        self.ext['PSD_den'] = feature_extractor_welchPSD(BASE_FOLDER,'v1')
        self.ext['PSD_den'].set_hyperparamter(nperseg=512, nfft=1024, channel='all', multichannel='stack')

        # outport ini
        self.outport_akkulist['MEL_den'] = []
        self.outport_akkulist['PSD_den'] = []
        #self.outport_akkulist['STFT_den'] = []
        pass
    
    def execute_diagram(self,file_path,file_class): # custom
        #-record target to akku append later
        #print(file_path)
        self.target_akkulist.append(file_class)
        
        #-
        denoise = feature_extractor_from_dict(self.pre['denoise'].get_dict(), self.base_folder)
        denoise.create_from_wav(file_path)
        #TODO STFT out
        
        #-
        MEL_den = feature_extractor_from_dict(self.ext['MEL_den'].get_dict(),self.base_folder)
        MEL_den.create_from_wav(denoise.get_wav_memory_file())
        self.outport_akkulist['MEL_den'].append(copy.deepcopy(MEL_den.get_dict()))
        #-
        PSD_den = feature_extractor_from_dict(self.ext['PSD_den'].get_dict(),self.base_folder)
        PSD_den.create_from_wav(denoise.get_wav_memory_file())
        self.outport_akkulist['PSD_den'].append(copy.deepcopy(PSD_den.get_dict()))
        pass