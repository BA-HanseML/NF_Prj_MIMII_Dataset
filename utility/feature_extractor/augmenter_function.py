def get_rand_fband():
    base = 500
    limit = 4500
    band = np.random.random_sample()*0.4
    frc = base + np.random.random_sample()*(limit -base)
    frc_u = frc*(1.+band)
    frc_l = frc*(1.-band)
    return frc_l, frc_u

def design_band_bass(sr,frc_l, frc_u):
    filtorder = 16*np.round(sr/frc_l)+1
    lower_trans = .1
    upper_trans = .1
    rand_increas = np.random.random_sample()*0.8
    rand_decreas = np.random.random_sample()*0.1
    filter_shape = [ 1-rand_decreas,1-rand_decreas,
                    1+rand_increas,1+rand_increas,
                    1-rand_decreas,1-rand_decreas ]
    filter_freqs = [ 0, frc_l*(1-lower_trans), frc_l, frc_u, \
                frc_u+frc_u*upper_trans,  sr/2 ]
    filterkern = scipy.signal.firls(filtorder,filter_freqs,filter_shape,fs=sr)
    return filterkern

def apply_filter(fker,s):
    return scipy.signal.filtfilt(fker,1,s) 

def aug_band_chain(s,sr,n=3):
    sout = s
    for i in range(n):
        frc_l, frc_u = get_rand_fband()
        fkern = design_band_bass(sr,frc_l, frc_u)
        sout = apply_filter(fkern,sout)
    return sout
    
def pitch_add(s,sr):
    return librosa.effects.pitch_shift(s, sr, n_steps=1)
    
    
def create_augmenter(wmf):
    import random 
    s = wmf.channel[0]
    pitch  = np.random.random_sample()>0.7
    bandadd = random.randint(2,6)
    if pitch:
        
        s = pitch_add(s, wmf.srate)
    
    s = aug_band_chain(s, wmf.srate, bandadd)
    
    wmf_r = memory_wave_file()
    wmf_r.filepath = wmf.filepath
    wmf_r.channel = [s]
    wmf_r.srate = wmf.srate
    wmf_r.length = len(s)
    return wmf_r