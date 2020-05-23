print('load feature_extractor_ICA2')

from sklearn.decomposition import FastICA

# Feature extractor for blind source separation from eight channels 
# to two and selecting the main channel based on the estimated mixing matrix

class feature_extractor_ICA2(feature_extractor):
    def __init__(self, base_folder, name='ICA2'):
        super().__init__(base_folder,name,
                        xlabel = 'time',
                        ylabel = 'amp',
                        zlabel = 'none')
        
        
        # set type
        self.para_dict['type'] = feature_extractor_type.ICA2
        self.para_dict['type_name'] = 'ICA2'
        # default hyper
        self.set_hyperparamter()
        
        self.wave_data = None
     
    def set_hyperparamter(self,
                           random_state=25):

        self.para_dict['hyperpara']={ \
                'random_state': random_state}
        

        if os.path.isfile(self._full_wave_path()):
                self.create_from_wav(self.para_dict['wave_filepath'] )
                
        
    def create_from_wav(self, filepath):
        
            transformer = FastICA(n_components=2, 
                random_state=self.para_dict['hyperpara']['random_state'])
                
            af = np.array(self._read_wav(filepath))
            afT = transformer.fit_transform(af.T)
            
            self.wave_data = afT.T
            self.feature_data = transformer.mixing_
            
    def get_wav_memory_file(self, main=False):
            
        wmf = memory_wave_file()
        wmf.filepath = self.para_dict['wave_filepath']
        if main:
            ica_range, ica_chnr, in_chnr = self._ICA_2_main_channel(self.feature_data)
            wmf.channel = self.wave_data[ica_chnr].reshape(1,-1)
        else:
            wmf.channel = self.wave_data
        wmf.srate= self.para_dict['wave_srate']
        wmf.length = self.feature_data.shape[1] 
        return wmf
        
    def _ICA_2_main_channel(self, mix_matrix):
        # returns dominat ica channel with the most mixing varaiton
        # and the dominate input channel mis that is directed to the device
        r = np.array([0.,0.])
        r[0] = np.abs(np.max(mix_matrix[:,0])- np.min(mix_matrix[:,0]))
        r[1] = np.abs(np.max(mix_matrix[:,1])- np.min(mix_matrix[:,1]))
        #print(mix_matrix[:,1])
        ica_range = np.max(r)
        ica_chnr = np.argmax(r)
        in_chnr = int(np.where(mix_matrix[:,ica_chnr]==np.min(mix_matrix[:,ica_chnr]))[0])
        return ica_range, ica_chnr, in_chnr 
        
    def flat_feature(self):
        return self.feature_data.flatten()
    
    def maxrange_feature(self):
            ica_range, ica_chnr, in_chnr = self._ICA_2_main_channel(self.feature_data)
            return ica_range
    
    def get_feature(self, feat_para_dict):
        if feat_para_dict['function'] == 'flat':
            return self.flat_feature()
        elif feat_para_dict['function'] == 'maxrange':
            return self.maxrange_feature()
        else:
             raise Exception('feat get function "' + feat_para_dict['function'] + '" unknown')