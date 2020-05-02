print('load Simple_FIR_HP')

class simple_FIR_HP():
    def __init__(self, fcut, sr):
        self.fcut=fcut
        self.filtb, self.filta = scipy.signal.butter(4,fcut/(sr/2),btype='high')
        self.sr = sr
        
    def plot_design(self):
        fs = self.sr

        impulse  = np.zeros(1001)
        impulse[501] = 1
        fimpulse = scipy.signal.filtfilt(self.filtb,self.filta,impulse)
        imptime  = np.arange(0,len(impulse))/fs
        
        plt.subplot(121)
        plt.plot(imptime,impulse,label='Impulse')
        plt.plot(imptime,fimpulse/np.max(fimpulse),label='Impulse response')
        plt.xlabel('Time (s)')
        plt.legend()
        plt.title('Time domain filter characteristics')
        
        
        # plot spectrum of IRF
        plt.subplot(122)
        hz = np.linspace(0,fs/2,3000)
        imppow = np.abs(scipy.fftpack.fft(fimpulse,2*len(hz)))**2
        plt.plot(hz,imppow[:len(hz)],'k')
        plt.plot([self.fcut,self.fcut],[0,1],'r--')
        plt.xlim([0,self.fcut*4])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.title('Frequency domain filter characteristics')
        plt.show()
     
    def apply(self,y):
        return scipy.signal.filtfilt(self.filtb,self.filta,y)
    
    def apply_multichannel(self,y):
        r = np.array([])
        for i in range(y.shape[0]):
            if i == 0:
                r = self.apply(y[i])
            else:
                r = np.vstack((r,self.apply(y[i])))
                
        return r