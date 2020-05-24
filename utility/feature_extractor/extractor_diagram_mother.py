print('load extractor_diagram_mother')

# Utility class that represents the baseline of a feature extraction diagram


import copy
class extractor_diagram():
    def __init__(self,base_folder,  threadnr=0 , main_channel=0,augment= -1, DeviceType=0, fHP = None ):
        
        # All common variable of an feature extraction diagram
        self.base_folder = base_folder
        self.threadnr = threadnr
        
        self.augment = augment
        self.DeviceType=DeviceType
        self.fHP = fHP
        self.main_channel =main_channel
        
        self.pre = {}
        self.ext = {}
        self.outport_akkulist = {} # one list per output port 
        self.target_akkulist = []        
        self.name = 'base'
        self.probe_port = {}
        self.ini_diagram()

        
    # Initialization of a specific diagram must be specified in derived class
    def ini_diagram(self): # custom

        
        pass
    #Execution process of a diagram must be specified in the derived
    def execute_diagram(self,file_path,file_class, probe=False): # custom

        pass
        

# Function to accumulate multiple output port 
# lists of a feature extraction diagram into one 
# list this is used to join the work from multiple threats back into one before saving it to file
def outport_akkulist_join(exdia_list=[]):
    ej = extractor_diagram('')
    ej.name = exdia_list[0].name
    for i,e in enumerate(exdia_list):
        if i==0:
           ej.outport_akkulist = e.outport_akkulist
           ej.target_akkulist = e.target_akkulist
        else:
            for op in e.outport_akkulist:
                ej.outport_akkulist[op] += e.outport_akkulist[op] 
            ej.target_akkulist += e.target_akkulist
    return ej

#Function to safe output port list of a feature extraction diagram to file 
#including the descriptive pandas data frame. 
import pandas as pd
def outport_akkulist_tofile(base_folder,target_folder,exdia,machine,SNR,ID):
    base_folder = os.path.abspath(base_folder)
    #print(base_folder)
    filename_base = machine + SNR + ID + '_' + exdia.name 
    outport_path = {}
    #data file
    for outport in exdia.outport_akkulist:
        outport_path[outport] = os.path.join(target_folder, filename_base + '_outp' + outport +'.pkl')
        filepath = os.path.abspath(base_folder+outport_path[outport])
        #print(outport)
        pickle.dump(exdia.outport_akkulist[outport],
                    open( filepath, "wb" ) )
    
    # Summery data frame
    #print('#1')
    df = pd.DataFrame()
    
    for outport in exdia.outport_akkulist:
        for i in range(len(exdia.outport_akkulist[outport])):
            #print(i)
            filepath = exdia.outport_akkulist[outport][i]['para_dict']['wave_filepath']
            #print(filepath)
            df.at[i,'path'] = filepath
            abnormal = exdia.target_akkulist[i]
            df.at[i,'abnormal'] = abnormal
            df.at[i,'datafile_idx'] = i
            df.at[i,outport] = outport_path[outport].replace('/','\\')
        
    df['SNR'] = SNR
    df['machine'] = machine
    df['ID'] = ID
    df['datafile_idx'] = df['datafile_idx'].astype('int32')
    summery_path = os.path.join(target_folder, filename_base + '_pandaDisc.pkl' )
    filepath = os.path.abspath(base_folder+summery_path)
    df.to_pickle(filepath)
    return df