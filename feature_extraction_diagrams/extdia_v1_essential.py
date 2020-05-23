print('load # extractor diagram V1 essential')

# Essential version for the final summary automation in the main notebook. 
#It contains only the winning prefilter and feature extraction from the development process.

class extdia_v1_essential(extractor_diagram):

    def ini_diagram(self): # custom
    
        # extractor diagram name
        self.name = 'EDiaV1'
        # name extention HP
        if self.fHP:
            self.name += 'HP'
        # name extention augment
        if self.augment>-1:
            self.name += 'aug' + str(self.augment)
            
        # name extention DeviceType ( Time Slicing or not)
        if self.DeviceType==1:
            self.name += 'TsSl'
        
        # extractor pre objects 
        self.pre['denoise'] = feature_extractor_pre_nnFilterDenoise(self.base_folder,'den')
        self.pre['denoise'].set_hyperparamter(aggregation=np.mean, channel=0)
        

        if self.fHP:
            self.pre['HP'] = simple_FIR_HP(self.fHP, 16000)
        else:
            self.pre['HP'] = simple_FIR_HP(120, 16000)
        
        
        # extractor objects
        
        self.ext['MEL'] = feature_extractor_mel(self.base_folder,'MELv1')
        self.ext['MEL'].set_hyperparamter(n_fft=1024, n_mels=80, hop_length=512, channel=0)
        
        self.ext['PSD'] = feature_extractor_welchPSD(BASE_FOLDER,'PSDv1')
        self.ext['PSD'].set_hyperparamter(nperseg=512, nfft=1024, channel=0)

        # outport ini

        self.outport_akkulist['MEL_raw'] = []
        self.outport_akkulist['PSD_raw'] = []
        self.outport_akkulist['MEL_den'] = []

        pass
    
    def execute_diagram(self,file_path,file_class, probe=False): # custom
        #-record target to akku append later
        
        # get file and cut main channel
        wmfs = [copy.deepcopy(memory_wave_file().read_wavfile(self.base_folder,file_path))]
        wmfs[0].channel = np.array([wmfs[0].channel[self.main_channel]])
        #print(wmfs[0].channel.shape )
        wmfs_class = [file_class]
        
        # react to augmenting flag 
        if file_class==self.augment:
            #print(file_class,self.augment,file_path)
            wmfs.append(create_augmenter(wmfs[0]))
            wmfs_class.append(-1)
        
        #print(wmfs[0].channel.shape)
        for wmf_i,wmf in enumerate(wmfs):
            #print(wmf_i,wmfs_class[wmf_i],file_path)
            self.target_akkulist.append(wmfs_class[wmf_i])
            
            #print(wmfs[wmf_i].channel.shape)
            # HP toggle on off
            if self.fHP:
                wmfs[wmf_i].channel[0] = self.pre['HP'].apply(wmf.channel[0])
            
            #print(wmfs[wmf_i].channel.shape)
            # Time Slice
            if self.DeviceType == 1:
                wmfs[wmf_i].channel = TimeSliceAppendActivation(wmfs[wmf_i].channel,wmfs[wmf_i].srate)
            
            #print(wmfs[wmf_i].channel.shape,file_path)
            # denoise 2
            
            self.pre['denoise'].create_from_wav(wmfs[wmf_i])
            wmf_den2 = copy.deepcopy(self.pre['denoise'].get_wav_memory_file())

            
            #->OUTPORTs
            self.ext['PSD'].create_from_wav(wmfs[wmf_i])
            self.outport_akkulist['PSD_raw'].append(copy.deepcopy(self.ext['PSD'].get_dict()))
            self.ext['MEL'].create_from_wav(wmfs[wmf_i])
            self.outport_akkulist['MEL_raw'].append(copy.deepcopy(self.ext['MEL'].get_dict()))
            
            self.ext['MEL'].create_from_wav(wmf_den2)
            self.outport_akkulist['MEL_den'].append(copy.deepcopy(self.ext['MEL'].get_dict()))
            
            
            
        pass