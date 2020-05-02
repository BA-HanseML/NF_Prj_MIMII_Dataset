print('load # extractor diagram V1')

class extdia_v1(extractor_diagram):

    def ini_diagram(self): # custom
    
        # extractor diagram name
        self.name = 'EDiaV0'
        
        # extractor pre objects 
        self.pre['denoise'] = feature_extractor_pre_nnFilterDenoise(self.base_folder,'den')
        self.pre['denoise'].set_hyperparamter(aggregation=np.mean, channel=0)
        
        self.pre['dereverb'] = WpeMethod(8, 1, 10)
        if self.fHP:
            self.pre['HP'] = simple_FIR_HP(self.fHP, 16000)
        else:
            self.pre['HP'] = simple_FIR_HP(120, 16000)
        
        
        # extractor objects
        self.ext['ICA2'] = feature_extractor_ICA2(self.base_folder,'ICA2')
        
        self.ext['MEL'] = feature_extractor_mel(self.base_folder,'MELv1')
        self.ext['MEL'].set_hyperparamter(n_fft=1024, n_mels=80, hop_length=512, channel=0)
        
        self.ext['PSD'] = feature_extractor_welchPSD(BASE_FOLDER,'PSDv1')
        self.ext['PSD'].set_hyperparamter(nperseg=512, nfft=1024, channel=0)

        # outport ini
        self.outport_akkulist['MEL_denbssm'] = []
        self.outport_akkulist['PSD_denbssm'] = []
        self.outport_akkulist['MEL_bssm'] = []
        self.outport_akkulist['PSD_bssm'] = []
        self.outport_akkulist['MEL_raw'] = []
        self.outport_akkulist['PSD_raw'] = []
        self.outport_akkulist['MEL_den'] = []
        self.outport_akkulist['PSD_den'] = []
        self.outport_akkulist['MEL_drvden'] = []
        self.outport_akkulist['PSD_drvden'] = []
        self.outport_akkulist['ICA_demix'] = []
        pass
    
    def execute_diagram(self,file_path,file_class, probe=False): # custom
        #-record target to akku append later
        
        # react to augmenting flag 
        wmfs = [copy.deepcopy(memory_wave_file().read_wavfile(self.base_folder,file_path))]
        wmfs_class = [file_class]
        
        if file_class==self.augment:
            #print(file_class,self.augment,file_path)
            wmfs.append(create_augmenter(wmfs[0]))
            wmfs_class.append(-1)
        
        for wmf_i,wmf in enumerate(wmfs):
            print(wmf_i,wmfs_class[wmf_i],file_path)
            self.target_akkulist.append(wmfs_class[wmf_i])
            
            # HP toggle on off
            wmfs[wmf_i].channel = self.pre['HP'].apply_multichannel(wmf.channel)
            
            # Main channel select
            wmfs_main = copy.deepcopy(wmfs[wmf_i])
            wmfs_main.channel = [wmfs_main.channel[self.main_channel]]
            
            #Drevert
            wmfs_drv = copy.deepcopy(wmfs[wmf_i])
            #wmfs_drv.channel = self.pre['dereverb'].run_offline(wmfs_drv.channel)
            
            #ICA2
            self.ext['ICA2'].create_from_wav(wmfs[wmf_i])
            #-> OUTPORT
            self.outport_akkulist['ICA_demix'].append(copy.deepcopy(self.ext['ICA2'].get_dict()))
            
            # denoise 1
            wmf_temp = self.ext['ICA2'].get_wav_memory_file(True)
            self.pre['denoise'].create_from_wav(wmf_temp)
            wmf_den1 = copy.deepcopy(self.pre['denoise'].get_wav_memory_file())
            
            # denoise 2
            self.pre['denoise'].create_from_wav(wmfs_main)
            wmf_den2 = copy.deepcopy(self.pre['denoise'].get_wav_memory_file())
            
            # denoise 3
            self.pre['denoise'].create_from_wav(wmfs_drv)
            wmf_den2 = copy.deepcopy(self.pre['denoise'].get_wav_memory_file())
            
            #->OUTPORTs
            self.ext['PSD'].create_from_wav(wmf_den1)
            self.outport_akkulist['PSD_denbssm'].append(copy.deepcopy(self.ext['PSD'].get_dict()))
            self.ext['MEL'].create_from_wav(wmf_den1)
            self.outport_akkulist['MEL_denbssm'].append(copy.deepcopy(self.ext['MEL'].get_dict()))
            
            
        pass