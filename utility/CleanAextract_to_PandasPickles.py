
# TODO get a cleaner inclusion maybe more then one
# TODO naming rule on the combination of extracrtor and Cleaner

import pandas as pd
import os
import sys
import glob
from tqdm import tqdm

def get_wave_files(base_folder,FileFindDict, FileCountLimit):
    
    fn = dict()
    fa = dict()
    SNR = FileFindDict['SNR']
    machine = FileFindDict['machine']
    ID = FileFindDict['ID']
    #print(base_folder, machine, SNR, ID)
    for idx in ID:
        
        fn[idx] = sorted(glob.glob(os.path.abspath( "{base}/{SNR}/{machine}/id_{ID}/{n}/*.{ext}".format(
        base=base_folder+'dataset',SNR=SNR,machine=machine,ID=idx, n='normal',ext='wav' ))))
    
        fa[idx] = sorted(glob.glob(os.path.abspath( "{base}/{SNR}/{machine}/id_{ID}/{n}/*.{ext}".format(
        base=base_folder+'dataset',SNR=SNR,machine=machine,ID=idx, n='abnormal',ext='wav' ))))
        
        
    for idx in fn:
        if FileCountLimit:
            if FileCountLimit < len(fn[idx]):
                fn[idx] = fn[idx][:FileCountLimit]
            if FileCountLimit < len(fa[idx]):
                fa[idx] = fa[idx][:FileCountLimit]
    
    return fn, fa

def BaseDataFrame(nf, af, FileFindDict):

    get_filename = lambda l: [os.path.basename(pl).replace('.'+'wav','') for pl in l]
    
    df = pd.DataFrame(columns=['path','abnormal','ID'])
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
    return df
    

def CleanAextract_to_PandasPickles(base_folder,
                                   target_folder,
                                   FileFindDict = {'SNR': '6dB',
                                                  'machine': 'pump', 
                                                  'ID': ['00']},
                                   FileCountLimit = None,
                                   CleanerObj = None,
                                   FeatureExtractorObj = None,
                                   verbose=1,
                                   ): 
    r"""Clean and extraction to pandas an pickles
    
    
    verbose : {0 ,1 ,2} optinal default is 1 list file names that have been processed , 2 gives progress bar
    
    Returns: None
    Will create a pkl Pandas table
    And a list of feature extracted channels
    CleanerObj -> FeatureExtractore -> to file
    """
    # TODO more input filter
    if FeatureExtractorObj==None:
        error('needs at least one FeatureExtractorObj')
    
    
    get_relpath = lambda pl: os.path.join(pl.replace(real_base_folder, ''))
    
    nf, af = get_wave_files(base_folder,FileFindDict, FileCountLimit)
    #print(nf)
    real_base_folder = os.path.abspath(base_folder)
    target_folder_full = os.path.abspath(real_base_folder + target_folder)
    
    
    # file name prefix based on type and key hyperparameter
    target_file_prefix=''
    if CleanerObj:
        target_file_prefix = CleanerObj.type_str + \
                             CleanerObj.name + '_' + \
                             CleanerObj.file_name_mainhyperparastr
        
    target_file_prefix =  target_file_prefix + \
                          FeatureExtractorObj.type_str + \
                          FeatureExtractorObj.name + '_' + \
                          FeatureExtractorObj.file_name_mainhyperparastr
    
    # create the base data frame
    df = BaseDataFrame(nf, af ,FileFindDict)
    
    
    # process the files
    if verbose == 2:
        l = tqdm(df.index)
    else:
        l = (df.index)
        
    for i in l:
        file_path = df.iloc[i]['path']
        if verbose==1:
            print(file_path)
            
        #
        #TODO add the cleaner and create form memory in extractor
        FEOloop = feature_extractor_from_dict(FeatureExtractorObj.get_dict(), base_folder)
        FEOloop.create_from_wav(file_path)
        
        file_name = target_file_prefix + '_' + \
                    df.iloc[i]['SNR']  + \
                    df.iloc[i]['machine'] + \
                    df.iloc[i]['ID'] + '_abn' +\
                    str(df.iloc[i]['abnormal']) + '_' +\
                    df.iloc[i]['file']+ '.pkl'
        
        FEOloop.save_to_file(os.path.abspath(target_folder_full+'/' + file_name))
        df.at[i, target_file_prefix] = target_folder + '\\' + file_name # TODO the backslash ...
     
    df.to_pickle(os.path.join(target_folder_full,'pandas_' + target_file_prefix))
    df['path'] = df['path'].apply(get_relpath)
    return df
    
    

    