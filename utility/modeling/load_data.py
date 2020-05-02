print('load load_data')

# main imports
import numpy as np
import pandas as pd
import os
import pickle

def load_data(path_descr, feat={'function':'flat', 'frames':3}
              , feat_col=None, SNR='6dB', machine='pump', ID='00'
              , train_set=True, BASE_FOLDER=BASE_FOLDER):
    
    df_descr = pd.read_pickle(path_descr)

    if not feat_col:
        poss_cols = [col for col in df_descr.columns 
                     if col not in ['path', 'abnormal', 'ID', 'file'
                                    , 'machine', 'SNR', 'train_set']]

        feat_col = input('Feature column not assigned, please define any of the following: \n' + '\n'.join(poss_cols)+'\n -->')

    msk = (df_descr.SNR==SNR) & (df_descr.machine==machine) & (df_descr.ID==ID) & (df_descr.train_set==int(train_set))
    df = df_descr[msk].copy()
    
    # unpack those features:
    # eventually blow up the descriptive dataframe 
    # for multi-channel or multi-frame features

    feature_files = df[feat_col].unique()
    
    i = 0
    
    for _file in feature_files:
        
        with open(BASE_FOLDER + _file, 'rb') as f_open:
            data_file = pickle.load(f_open)
            
            for _datafile_idx in df[df[feat_col] == _file].datafile_idx.unique():
                
                # create the feature extractor class
                feat_extractor_ = feature_extractor_from_dict(data_file[_datafile_idx], BASE_FOLDER)

                newax = False
                # append the feature data
                if i == 0:
                    # read first set and instantiate data array
                    num_files = len(df[feat_col])
                    first_data = np.atleast_2d(feat_extractor_.get_feature(feat))
                    num_instances = first_data.shape[0]
                    data = np.zeros((num_instances*num_files, first_data.shape[1]))
                    data[0:num_instances,:] = first_data
                    
                    # create the dataframe accordingly
                    multiplier_frame = pd.DataFrame([[ID, i] for i in range(0, num_instances)], columns=['ID', feat['function']])
                    df['file_idx'] = df.index
                    df = pd.merge(df, multiplier_frame, on='ID', how='outer')
                    
                else:
                    data[num_instances*i:num_instances*(i+1), :] = np.atleast_2d(feat_extractor_.get_feature({'function':'frame', 'frames':5}))
                
                # next instance
                i += 1

    return df, data