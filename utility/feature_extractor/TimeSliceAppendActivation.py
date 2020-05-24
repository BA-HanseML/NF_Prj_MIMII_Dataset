print('load TimeSliceAppendActivation')

# Utility function that implements time slicing based on activity detection. 

from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import librosa


def time_to_index(t,sr,l):
    te=l/sr
    t_fract = t/te
    return int(l*t_fract)
    


def TimeSliceAppendActivation(y, sr, fn=''):
    # create STFT
    ch_stft = librosa.stft(y[0], n_fft =1024,hop_length =512, win_length = 1024)
    t_f = np.linspace(0,len(y[0])/sr,ch_stft.shape[1])
    D = librosa.amplitude_to_db(np.abs(ch_stft), ref=np.max)
    
    # std scale the STFT
    scaler = StandardScaler()
    Dscaled = scaler.fit_transform(D.T)  # we cluster time frames 
    
    
    #PCA the scaled STFT
    pca = PCA(n_components=15)   
    X = pca.fit_transform(Dscaled)
    
    # kmean over reduced time frames
    n = 2 # on and off
    kmean= KMeans(n_clusters=n, max_iter=600, tol=0.001,random_state=25)
    kmean.fit(X)
    
    # define the starting points by the cluster with the least members
    unique_elements, counts_elements = np.unique(kmean.labels_, return_counts=True)
    c_on = np.argmin(counts_elements)
    c_off = np.argmax(counts_elements)
    
    # lame version of finding the range of a activation
    ranges_s = np.array([])
    ranges_e = np.array([])
    ii = 0
    last = 0
    for i in np.where(kmean.labels_==c_on)[0]:
        if i-last > 1:
            if i > 3:
                ii = i-3
            else:
                ii = i
            ranges_s = np.append(ranges_s,t_f[ii])
        
            for j in np.where(kmean.labels_==c_off)[0]:
                if j>i:
                    if j+4 < len(np.where(kmean.labels_==c_off)[0]):
                        jj= j+4
                    else:
                        jj = len(np.where(kmean.labels_==c_off)[0])-1
                        
                    ranges_e = np.append(ranges_e,t_f[jj])
                    break
    
        last = i
     
    # using the time slices marker to remerge to full time
    out = np.array([])
    for i in range(y.shape[0]):
        new_audio = np.array([])
        #noise_audio = np.array([])
        #last_e = 0
        for a_ts, a_te in zip(ranges_s, ranges_e):
            i_s = time_to_index(a_ts,sr,len(y[i]))
            i_e = time_to_index(a_te,sr,len(y[i]))
            new_audio = np.append(new_audio, y[i][i_s:i_e])
            #noise_audio = np.append(noise_audio, y[0][last_e:i_s])
            #last_e = i_e
        
        if len(new_audio) > 0:
            new_audio_app = np.array([])
            r_len = int(np.ceil(len(y[0])/len(new_audio)))
            for j in range(r_len):
                new_audio_app = np.append(new_audio_app, new_audio)
                new_audio_app = new_audio_app[:len(y[0])]  
        else:
            print('message from time slicer:',i, fn)
            new_audio_app = y[i] # if slicing failed
        
        if i==0:
            #print(out)
            out = np.array([new_audio_app])
        else:
            out = np.vstack((out,new_audio_app))

    return out
    
    # -- MISC --- for adaptiv filter extract the noise floor
    #noise_audio_app = np.array([])
    #r_len = int(np.ceil(len(y[0])/len(noise_audio)))
      
    #for i in range(r_len):
    #    noise_audio_app = np.append(noise_audio_app, noise_audio)
    #noise_audio_app = noise_audio_app[:len(y[0])]