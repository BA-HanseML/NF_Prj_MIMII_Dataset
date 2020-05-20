
# Improvements / Future work on the detection algorithm

This section reflects on open topics for the detection, with a focus on how to improve performance and robustness.

## feature extraction

### Time Slicing / activation Time Detection

the current algorithm works by assuming that a clustering kNN will find two main cluster active and inactive in the raw data. This assumption maybe to naive in some noise situation and has shown to be not robust with slider rails. 

One way to improve this is by using more cluster and the check for total signal power in that time frame. 

Or trying to use sequences instate of unsorted time frames.

Or just finding onset than analyse the following time frames separated and find the end of activation.

More experiments with light denoising could make this more robust.

Further the current approaches fills up the 10 sec frame with active time this would not be necessary if the rest of the chain could deal with flexible length of recordings or just deals with a continues stream. For use of the MIMII the audio files would then be appended to one long file - this also would aid in simulating a more real time like scenario.

### Main Channel and Direction (DOA)

In some experiments it was possible to show that DOA algorithms can point to the machine part even in high noise. DOA need multiple microphones best as ring as used in the MIMII they also point out that sparse filter could be use to isolate the machine in more advanced way from the noise. But at least they leave proof that is possible to automatically choice the microphone pointing most to the machine without knowing the azimuth alignment of the microphone ring.

### Downsampling

in some cases, indicators can be found that down sampling could be option to increase performance. A PCA of the PSD can maybe help to find the new sample frequency but this is risky for robustness.

### Denoising

More blind denoising variants might be worth testing also in the goal of real time implementation. As the used nn filter needs a lot of loops to find the best convolution as to reconstruct the STFT from a noised one.

A further interesting approached would be to use background noise estimation based on the activation time. When the none active time frames are known none blind denoising can be used like adaptive filters or STFT based ones like the [Audacity Noise Reduction](https://wiki.audacityteam.org/wiki/How_Audacity_Noise_Reduction_Works)

### Pre Filter
We used high pass and it can be seen that some of structural born noise is blurring the attention from the airborne noise. Experiments need to be done what really helps and what hurts for the high pass filter, to little work is done for verification of this step, right now it is added on good measure bases.

### Dereverb

Dereverb can be done on the spectrum wit cepstrum correlation and delay estimation between microphones or even recordings. We found indication of improvement when experimenting with the MPE algorithm but way to little work is done to draw conclusion. Dreverb is hard signal processing problem by it self but maybe very interesting in factory space where there are likely reverberative surfaces like metal plates and stone walls with very little acoustic damping.

### Cepstrum and MFC

In speech recognition the mel frequency cepstrum is used very successful since the cepstrum can show where frequencies are changing in time domain. This Cepstrum analyses feature did seem as helpful for the task at hand here but more investigation into it may reveal otherwise as the research was done very shallow on this end. Also, since no sequence detection was used for the classification it may not been able to reveal its true potential.



