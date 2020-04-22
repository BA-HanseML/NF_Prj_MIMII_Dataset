print('load audition_function_main')

def audtion_display_path(filepath):
    display(Markdown('#### ' + filepath))



def make_audition_list(df_select,
                       base_folder=r'./',
                       no_section = False,
                       listen=True,
                       listen_every=1, # buggy for now
                       listen_stereo_ch=[0,4],
                       time_plot_ch = -1, # turn of by setting -1
                       psd_from_data = False,
                       psd_from_data_dB = True,
                       fft_from_data = False, # not there
                       Combine_psdfft = False, # maybe changhe to have both
                       Combine_psdfft_hue = 'abnormal', # not fully implemented legend missing
                       Combine_psdfft_hue_colormap = None, # not forwarded
                       mel_from_data = False,    # not there
                       mel_create = False,
                       mel_create_para = {'n_mels':64, 
                                     'n_fft':1024,
                                     'power':2.0,
                                    'hop_length':512}, # expects mel paramters
                       ):
    
    # akku classes
    if Combine_psdfft:
        psd_akkuplot = audition_akku_plot('freq. [Hz]', 'V^2') # TODO dB 
    
    for row in range(len(df_select.index)):
        
        # Dispaly main section and possible audio player
        if listen:
            if row%listen_every==0:
            
                audition_listion(df_select.path.iloc[row], 
                             base_folder, 
                             listen_stereo_ch, 
                             time_plot_ch)
            plt.show()
        else: 

            if time_plot_ch > -1:
                audition_listion(df_select.path.iloc[row], 
                             base_folder, 
                             listen_stereo_ch, 
                             time_plot_ch,play=False)
                plt.show()
            else:
                if not no_section:
                    audtion_display_path(df_select.path.iloc[row])
            
        df_row = df_select.iloc[row]    
        # create single psd for every section
        
        if psd_from_data and not Combine_psdfft:
            if row%listen_every==0:
                audition_psd_from_data_plot(df_select.iloc[row], psd_from_data_dB)
                plt.show()
        
        if mel_create:
            fe_mel = feature_extractor_mel(base_folder)
            fe_mel.create_from_wav(df_select.path.iloc[row])
            fe_mel.plot()
            plt.show()
        
        
        # akku psd
        if psd_from_data and  Combine_psdfft:  
            hue_info = df_row[Combine_psdfft_hue]
            x, y = audition_psd_from_data(df_row, psd_from_data_dB)
            # TODO name ...
            psd_akkuplot.add_line(x,y,'#',hue_info)
          
        
        
    if psd_from_data and  Combine_psdfft:
        psd_akkuplot.plot() # TODO react on hue