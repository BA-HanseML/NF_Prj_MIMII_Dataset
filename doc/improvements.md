
# Improvements / Future Work On the Detection Algorithm

This section reflects on open topics for the detection, with a focus on how to improve performance and robustness.

## Feature Extraction

### Time Slicing / Activation Time Detection

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



## Modeling

### Pseudo-supervised

The main problem with the pursuit of supervised approach used in the study is that it fits too well in training, this indicates that the augmentation is too easy to distinguish from normal. Nonetheless it was good enough to create a decent detector. But it also points to many possibilities of improvement like:

By incorporating the augmentation directly into the learning loop, thereby creating an adversary feedback loop. This means that the training result of the supervised classifier is taken into a tuning function for the augmentation and after tuning the augmentation the next training is conducted with the goal to reach a low training score with the assumption in mind that a particularly hard to distinguish syntactic abnormal would be harder to distinguish than the real abnormal.

This might be achievable with convolution layouts. In case this would be successful a convolution a neural network could be used in U-net architecture to emphasize the abnormal parts in a spectra. 

On the problem of the used augmentation is that it is applied throughout the entire time of one file in this case 10 seconds. If the augmentation would also be randomized by time or simply asked a convolution on the STFT the approach can even be used when sequential modeling is as used.

Thereby many opportunities have to be explored and the study is only showing of very simple version of the pseudo-supervised approach.

### Unsupervised Modeling

#### Boosting of Stochastic Models
Speaking of the unsupervised approach the stochastic models delivered promising results but were outperformed by the Autoencoder. Still in the ensemble the combination of all models scores increased. In [1] they used Gaussian Mixture Models in a boosting ensemble to increase the performance if an anomaly detection algorithm. This approach could be transfered to this study

#### Autoencoder Including Sequence-based Models - LSTM-Autoencoder
All of the models chosen in this study do not utilize the time information. We assume especially sporadic machinery would benefit from including sequence-based models like LSTM layers to an LSTM-Autoencoder.

#### Investigate Deployability
As this study is a proof-of-concept not much emphasis was placed on deployability. This should definitely be investigated. Especially the stochastic models performance in an embedded device should be examined.

#### DSP Embedding Layers for Autoencoder
The approach to firstly extract all the features from the data favored performance in training the individual models. But in a proof-of-work one would need to introduce online-feature-extraction. TensorFlow delivers an extensive subpackage of digital signal processing functionality. Including these into the ensemble for online functionality is future work.

### Ensemble

#### Optimization of the Blender

Hence the goal of this study is to find the most robust detection algorithm over all types of machinery, tuning hyperparameters could be applied on a subset of the data. Like we used the subset of IDs 00 and 02 to find the most promising individual models for the ensemble, one could also tune the blender-weights of all the individual models to get the best set for the ensemble. Evaluation could be done with the remaining subset of the data (e.g. ID 04 and 06).

#### Including Toggleable Submodels

In a possible application one could add toggleable submodels that perform very well on specific tasks. For example we found out that activation time detection improved results for sporadic machinery a lot but doesn't support the anomaly detection for continuous machinery. To add toggleable submodels to adjust the model for a specific task should deliver good results at the cost of robustness, since the solution is specifically customized for a certain task.

# References

[[1]](https://www.semanticscholar.org/paper/Detection-of-Abnormal-Sound-Using-Multi-stage-GMM-Ito-Aiba/27628c9aeecb4df6010693533ad79f4d03c64f86) Ito, Akinori, Akihito Aiba, Masashi Ito and Shozo Makino. “Detection of Abnormal Sound Using Multi-stage GMM for Surveillance Microphone.” 2009 Fifth International Conference on Information Assurance and Security 1 (2009): 733-736.