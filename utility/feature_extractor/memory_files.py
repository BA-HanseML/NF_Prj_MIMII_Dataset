class memory_wave_file():
    def __init__(self):
        self.filepath = ''
        self.channel = None
        self.srate = 0
        self.length = 0
    
    def read_wavfile(self, base_folder, file_path):
        #print('#')
        filepath = file_path.replace(os.path.abspath(base_folder),'')
        #print('#')
        self.filepath = filepath
        #print('#')
        af, sr = librosa.load(os.path.abspath(base_folder+filepath), sr=None, mono=False)
        
        #print(af.shape)
        self.srate = sr
        self.length = len(af[0])
        self.channel = af
        return self
     

    