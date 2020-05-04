print('Load split_data')

# main imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def split_index(indeces, labels, files):
    '''
    Will combine the testset from all abnormal operation data
    and add up the same amount of normal operation data
    the remaining will be the training dataset
    
    indeces: array-like
        Indeces of descriptive table or dataframe
        
    labels: array-like
        Labels whether instance is abnormal (label==1 indicates abnormal instance)
    '''

    # get indices
    idx_abnormal = indeces[labels==1]
    idx_augmented = indeces[labels==-1]
    idx_normal = indeces[labels==0]
    
    # split the normal data
    num_abnormal = len(idx_abnormal)
    idx_train, idx_test_normal = train_test_split(idx_normal, test_size=num_abnormal)

    # the testset contains all abnormal operation data
    idx_test = idx_test_normal.union(idx_abnormal)
    
    # the respective augmented file in the test-set should not appear in train-set
    files_test_normal = files[idx_test_normal]
    files_augmented = files[idx_augmented]
    idx_augmented_test = idx_augmented[files_augmented.isin(files_test_normal)]
    
    idx_train = idx_train.union(idx_augmented)

    return idx_train, idx_test, idx_augmented_test


def tt_split(table_path):
    '''
    Reads desciptive table from pickle, splits it into training and testing dataset.
    Returns table with additional column with training/testing index.
    
    table_path: string
        Path to the descriptive dataframe
    '''

    table = pd.read_pickle(table_path)

    SNRs = table.SNR.unique()
    machines = table.machine.unique()
    IDs = table.ID.unique()

    if 'train_set' in table.columns:
        table = table.drop(columns=['train_set'])

    # initialize the new column
    tt_series = pd.Series(0, index=table.index,
                            name='train_set', dtype=np.int8)

    # split for every individual ID, machine and SNR
    for SNR in SNRs:
        for machine in machines:
            for ID in IDs:

                # create the individual mask 
                # and read the indeces and labels accordingly
                mask = (table.SNR == SNR) & (
                    table.machine == machine) & (table.ID == ID)
                
                idx = table[mask].index
                labels = table[mask].abnormal
                files = table[mask].path

                # get the indeces that belong to the training dataset 
                # and update the new column
                idx_train, _, idx_augmented_test = split_index(idx, labels, files)
                tt_series[idx_train] = 1
                tt_series[idx_augmented_test] = -1
                

    table = table.join(tt_series)
    table.to_pickle(table_path)

    print('{} --> Done'.format(table_path))