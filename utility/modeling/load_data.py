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

    for i, file in enumerate(tqdm(df[feat_col])):

        # create the feature extractor class
        feat_extract_ = feature_extractor_from_file(
            BASE_FOLDER+file, BASE_FOLDER)

        newax = False
        # append the feature data
        if i == 0:
            # read first set and instantiate data array
            num_files = len(df[feat_col])
            first_data = np.atleast_2d(feat_extract_.get_feature(feat))
            num_instances = first_data.shape[0]
            data = np.zeros((num_instances*num_files, first_data.shape[1]))
            data[0:num_instances,:] = first_data
            
            # create the dataframe accordingly
            multiplier_frame = pd.DataFrame([[ID, i] for i in range(0, num_instances)], columns=['ID', feat['function']])
            df['file_idx'] = df.index
            df = pd.merge(df, multiplier_frame, on='ID', how='outer')
            
        else:
            data[num_instances*i:num_instances*(i+1), :] = np.atleast_2d(feat_extract_.get_feature({'function':'frame', 'frames':5}))

    return df, data