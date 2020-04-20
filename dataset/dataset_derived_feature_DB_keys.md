# derived feature DB

any derived feature DB is a pandas data frame with some main keys to identify the indevitual wav file it corresponds to.

## file naming rule
<machine>_<SNRs>_<IDs>_<name of feature and key paramter>
i.e: pump_0dB_00020406_full_spectrum_128.pkl
pump_0dB6DB_00020406_full_spectrum_128.pkl


name of feature and key paramter is a free text but should indicate what is insite
### log book of name of feature


## main key 

the main keys must be in every table as most post scripts are in need of it

### path (the most important key!)
name: 'path'
description: is the relativ path to the wav file
i.e: '\dataset\min6dB\fan\id_04\normal\00000503.wav'
notice: the most work was done on a windows system and the path can be trasnforemde by os.path if used as path, but it also serves as unique identifyer for pandas frame joining!


### abnormal (the main target)
name: 'abnormal'
description: 0 for normal and 1 for abnormal

### ID
name: 'ID'
description: a sting of two digits corresponding to the id of the machine of a type i.e. '00' or '04'

### SNR
name 'SNR'
description: a string like part of folder for the sound to noise ration i.e. '6dB' or 'min6dB'


## otional main keys

optinal keys are additionl infos

### file
name: 'file'
description: only file name

### SNRn
name 'SNRn'
description: SNR as indeger


## manual cluster keys

by clustering the normal recordings and the abnormal recordings some clear diffrences are noticable this are diffrent cluster sets
from purly unsupervised cluster analyses: 

### pump
TODO
find csv here: TODO


## feature identification

### float64 type frequncy 
name: <flaot64> number
description: used to have welch spectrum directly in the pandas frame each columan is then a freq.

### PSD_f_
name: PSD_f_<ident>
description: file path to two pickeled np.array's first for power and secound for freq. bins
ident: some name or number 

### MEL_f_ Mel spectra
name: SD_f_<ident>
description: file path to two pickeled np.array's of mel spectra as defiened by librosa package
ident: some name or number 


