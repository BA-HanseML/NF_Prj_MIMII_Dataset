print('load feature_extractor_mother')

def Plain_Spectraplot(data):
    pass
    
def Plain_freqplot(data):
    pass


from enum import Enum
class feature_extractor_type(Enum):
    BASE = 0
    PSD = 1
    MEL_SPECTRUM = 2
    WELECHPSD = 3


# TODO load based on columns header

class feature_extractor_memory_wave_file():
    def __init__(self):
        self.filepath = ''
        self.channel = None
        self.srate = 0
        self.length = 0


def feature_extractor_from_dict(d, base_folder):
    #print(d)
    if d['para_dict']['type'] == feature_extractor_type.MEL_SPECTRUM:
        fe = feature_extractor_mel(base_folder)
        fe.read_from_dict(d)
    if d['para_dict']['type'] == feature_extractor_type.WELECHPSD:
        fe = feature_extractor_welchPSD(base_folder)
        fe.read_from_dict(d)
    return fe
    
def feature_extractor_from_file(filepath, base_folder):
    d = pickle.load( open( filepath, "rb" ))
    return feature_extractor_from_dict(d,base_folder)

class feature_extractor():
    def __init__(self,base_folder, name='base_feature', xlabel='x', ylabel='y',zlabel='z'):
        self.para_dict = \
        {'name': name,
         'xlabel': xlabel,
         'ylabel': ylabel,
         'zlabel': zlabel,
         'type_name': 'BASE',
         'data_channel_use_str': '',
         'type': feature_extractor_type.BASE,
         'file_name_mainhyperparastr': '',
         'wave_filepath': '',
         'wave_srate': 0,
         'wave_length': 0,
         'wave_channel': [0],
         'hyperpara':{}}
        self.base_folder= base_folder
        self.feature_data = None
    
    @property
    def name(self):
        return  self.para_dict['name']
        
    def __str__(self):
         return '<'+str(self.para_dict['type']) + '>[' + \
                str(self.para_dict['hyperpara']) + ']' + \
                'wav=' +str(self._full_wave_path())
     
    def set_hyperparamter(self):
         pass
    
    def set_hyperparamter_from_fe(self,fe):
        self.para_dict['hyperpara'] = fe.para_dict['hyperpara']
        pass
    
    def _full_wave_path(self,filepath=None):
        if filepath:
            return os.path.abspath(self.base_folder+filepath)
        else:
            return os.path.abspath(self.base_folder+self.para_dict['wave_filepath'])
        

    
    def _read_wav(self, filepath):
        if type(filepath) is str:
            filepath = filepath.replace(os.path.abspath(self.base_folder),'')
            self.para_dict['wave_filepath'] = filepath
            af, sr = librosa.load(self._full_wave_path(filepath), sr=None, mono=False)
            self.para_dict['wave_srate'] = sr
            self.para_dict['wave_length'] = len(af[0])
        else: # TODO make this more robust but 
            self.para_dict['wave_filepath'] = filepath.filepath.replace(os.path.abspath(self.base_folder),'')
            af  = filepath.channel
            self.para_dict['wave_srate'] = filepath.srate
            self.para_dict['wave_length'] = len(af)
            
        return af
        
    def create_from_wav(self, filepath, channel):
        
        pass
        
    def read_from_dict(self, d):
        self.para_dict = d['para_dict']
        self.feature_data = d['feature_data']
        pass
    
    def get_dict(self):
        return {'para_dict': self.para_dict,
                'feature_data': self.feature_data}
    
    def save_to_file(self, filepath):
        pickle.dump(self.get_dict(),
                    open( filepath, "wb" ) )
        # TODO catch errors and ahndling
        pass
        
    def plot(self):
        print('nothing to plot')
        pass
        
    def plot_data(self):
        pass
   
        
    def flat_feature(self):
        pass
        
    @property   
    def file_name_mainhyperparastr(self): # returns a string for filename that descripes the most importand hyper parmater like window length etc.
        return self.para_dict['file_name_mainhyperparastr'] 
    
    @property
    def type_str(self): # returns a str for filename type of extractor MEL PSD etc.
        return self.para_dict['type_name'] 
    
    @property
    def data_channel_use_str(self): # returns a sting for filename use of channels like how many and concat or stacked
        return self.para_dict['data_channel_use_str']