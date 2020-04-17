import scipy.signal as sig
import numpy as np
import librosa
import pandas as pd

import os
import sys
import glob


def get_files(base_folder,SNR,machine,ID):
    
    fn = dict()
    fa = dict()
    
    for idx in ID:
        
        fn[idx] = sorted(glob.glob(os.path.abspath( "{base}/{SNR}/{machine}/id_{ID}/{n}/*.{ext}".format(
        base=base_folder+'dataset',SNR=SNR,machine='pump',ID=idx, n='normal',ext='wav' ))))
    
        fa[idx] = sorted(glob.glob(os.path.abspath( "{base}/{SNR}/{machine}/id_{ID}/{n}/*.{ext}".format(
        base=base_folder+'dataset',SNR=SNR,machine='pump',ID=idx, n='abnormal',ext='wav' ))))
    
    return fn, fa
    

def PSD_to_Pandas(PSD_window='hamming',
                  PSD_nperseg = 128,
                  PSD_nfft=512,
                  PSD_scaling='spectrum',
                  freq_band = [0,16000],
                  base_folder = './',
                  FileFindDict={'SNR': '6dB',
                                'machine': 'pump', 
                                'ID': ['00']},
                  ChannelNr=0,
                  FileCountlimit=None):
    
    # get file path
    nf, af = get_files(base_folder,
                       FileFindDict['SNR'],
                       FileFindDict['machine'],
                       FileFindDict['ID'])
    
    # limit the File count
    for idx in nf:
        if FileCountlimit:
            if FileCountlimit < len(nf[idx]):
                nf[idx] = nf[idx][:FileCountlimit]
            if FileCountlimit < len(af[idx]):
                af[idx] = af[idx][:FileCountlimit]
     
    # create base pandas
    real_base_folder = os.path.abspath(base_folder)
    df = pd.DataFrame(columns=['path','abnormal','ID'])
    
    get_filename = lambda l: [os.path.basename(pl).replace('.'+'wav','') for pl in l]
     
    for idx in nf:
        df_temp_n = pd.DataFrame()
        df_temp_n['path'] = nf[idx]
        df_temp_n['file'] = get_filename(nf[idx])
        df_temp_n['abnormal'] = 0
        df_temp_n['ID'] = idx
        df_temp_a = pd.DataFrame()
        df_temp_a['path'] = af[idx]
        df_temp_a['file'] = get_filename(af[idx])
        df_temp_a['abnormal'] = 1
        df_temp_a['ID'] = idx
        df = df.append(df_temp_n, ignore_index = True) 
        df = df.append(df_temp_a, ignore_index = True) 
    
    df['machine'] = FileFindDict['machine']
    df['SNR'] = FileFindDict['SNR']
    
    
    # create the psd columns
    first_loop = True
    for i in df.index:
        file_path = df.iloc[i]['path']
        #print(file_path)
        audio_ch, sr = librosa.load(file_path, sr=None, mono=False)
        f, Pxx = sig.welch(audio_ch[ChannelNr],sr,
                           window=PSD_window,
                           nperseg=PSD_nperseg, 
                           noverlap=False, 
                           nfft=PSD_nfft,
                           scaling=PSD_scaling)

        if first_loop:
            first_loop = False
            if freq_band[0] > 0:
                idx_s = np.min(np.where(f>freq_band[0]))
            else:
                idx_s = 0
                
            if freq_band[1] < np.max(f):
                idx_e = np.min(np.where(f>freq_band[1]))
            else:
                idx_e = len(f)
                
            # basic matrix    
            ff = f[idx_s:idx_e]    
            PSDmatrix = np.zeros([len(df.index),len(ff)])
            
       
        for iF,Pi in enumerate(Pxx[idx_s:idx_e]):
             PSDmatrix[i,iF]=Pi
            

        
    df_psd = pd.DataFrame(columns=ff,data=PSDmatrix)
    # make path relativ to project
    get_relpath = lambda pl: os.path.join(pl.replace(real_base_folder, ''))
    df['path'] = df['path'].apply(get_relpath)
    return pd.concat([df,df_psd], axis=1)