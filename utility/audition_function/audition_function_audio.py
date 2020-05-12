print('load audition_function_audio')

# just create audio player from IPython audio
def audition_listion(filepath, base_folder, stereo_ch=[0,4], time_plot_ch = 0, play=True):
    audtion_display_path(filepath + ' ch:' + str(stereo_ch))
    audio_ch  = \
            librosa.load(os.path.abspath(base_folder+filepath), sr=None, mono=False)
    
    if len(stereo_ch) == 1:
        stereo_ch.append(stereo_ch[0])
    elif stereo_ch == None:
        stereo_ch == [0,0]
    
    if time_plot_ch > -1:
        librosa.display.waveplot(audio_ch[0][time_plot_ch],
                                                 sr=audio_ch[1])
        plt.grid()
        
    if play:
        display(Audio(data=[audio_ch[0][stereo_ch[0]], \
                            audio_ch[0][stereo_ch[1]]], \
                  rate=audio_ch[1]))