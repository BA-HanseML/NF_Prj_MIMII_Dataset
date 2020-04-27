def unpack_features(list_of_files, BASE_FOLDER, feat):

    for i, file in enumerate(tqdm(list_of_files)):

        # create the feature extractor class
        fe_mel_read = feature_extractor_from_file(
            BASE_FOLDER+file, BASE_FOLDER)

        # append the feature data
        if i == 0:
            feat_data = fe_mel_read.get_feature(feat)[
                np.newaxis, :]
        else:
            feat_data = np.append(feat_data,
                fe_mel_read.get_feature(feat)[
                np.newaxis, :], axis=0)

    return feat_data

def load_data(path_descr, feat={'function:':'flat', 'frames':5}, feat_col=None, SNR='6dB', machine='pump', ID='00', train_set=True, BASE_FOLDER=BASE_FOLDER):
    df_descr = pd.read_pickle(path_descr)

    msk = (df_descr.SNR==SNR) & (df_descr.machine==machine) & (df_descr.ID==ID) & (df_descr.train_set==int(train_set))
    df = df_descr[msk].copy()
    
    return df, unpack_features(df[feat_col], BASE_FOLDER, feat=feat)