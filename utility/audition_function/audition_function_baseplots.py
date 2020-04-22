print('load audition_function_baseplots')


        
def audition_psd_plot(x,y,df_row, dB=True):  
    plt.plot(x,y)
    plt.grid()
    plt.title(f'psd {df_row.machine} id:{df_row.ID} snr:{df_row.SNR}')
    plt.xlabel('frequency [Hz]')
    if dB:
        plt.ylabel(' 10*log10(V**2)')
    else:
        plt.ylabel(' V**2 ')
        
def audition_psd_from_data(df_row, dB=True):
    #df_row=df.iloc[box_idx].iloc[0]
    y = df_row[[type(e) is float for e in df_row.index]]
    x = y.index.values.astype('float')
    if dB:
        y = 10*np.log10(y.values.astype('float'))
        
    return x,y
    
def audition_psd_from_data_plot(df_row, dB=True):
    x, y = audition_psd_from_data(df_row, dB)
    audition_psd_plot(x,y,df_row, dB)