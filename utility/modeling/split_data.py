def split_index(indeces, labels):
    
    '''
    Will combine the testset from all abnormal operation data
    and add up the same amount of normal operation data
    the remaining will be the training dataset
    
    indeces: indeces of descriptive table or dataframe
    labels: labels whether instance is abnormal (label==1 - abnormal)
    '''

    idx_abnormal = indeces[labels==1]
    num_abnormal = len(idx_abnormal)
    
    idx_normal = indeces[labels==0]
    idx_train, idx_test_normal = train_test_split(idx_normal, test_size=num_abnormal)

    # the testset contains all abnormal operation data
    idx_test = idx_test_normal.union(idx_abnormal)

    return idx_train, idx_test


def tt_split(table_path):
    '''
    Reads desciptive table from pickle, splits it into training and testing dataset.
    Returns table with additional column with training/testing index
    '''

    table = pd.read_pickle(table_path)

    SNRs = table.SNR.unique()
    machines = table.machine.unique()
    IDs = table.ID.unique()

    if 'train_set' in table.columns:

        print('{} --> Train test split already done, passed'.format(table_path))

    else:

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

                    # get the indeces that belong to the training dataset 
                    # and update the new column
                    idx_train, _ = split_index(idx, labels)
                    tt_series[idx_train] = 1

        table = table.join(tt_series)
        table.to_pickle(table_path)

        print('{} --> Done'.format(table_path))