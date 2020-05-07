# Feature Extraction 

## Introduction 

Audio feature extraction is the diverse set of filters to get features extracted from the raw recording ready for a machine learning algorthem to process it. While cleaning operation like de-noising or de-reverbing are done. Further, it can be attempted to use multi channel recordings that are done with spatial separated microphone arrays, like this dataset is recorded with 8 microphones in a circle.  The feature could be formulated in the time domain but usually are left in frequency domain so that the output is a form of the spectrum like Welch in 1D or a STFT or alike in 2D. Other outputs are possible like envelopes BSS (blind source separation) de-mixing estimations or DOA (direction of arrival) as well as basic statistics like SNR (sound to noise ratio) estimation or standard deviation etc.

In this study, we settled with:
* MEL spectrum
* Welch spectrum ( called PSD here, even then, even if not it is not the density, but the spectral power V^2 instead of V^2/f)
* FastICA mixing matrix estimation

We also explored other forms find below remarks to that exploration.

For pre-filtering we settled:
* nn-filter denoising
* FastICA
* K means clustering on STFT to find activation

Further audio augmentation for pseudo supervision is a topic in feature extraction.

In the documentation many links lead to Jupyter notebooks in the the folder feature_extraction_diagrams.


## Diagrams


## Pre Pre Processing and Time Sliceing