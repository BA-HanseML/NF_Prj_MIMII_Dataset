# Feature Extraction 

## Introduction 

Audio feature extraction is the diverse set of filters to get features extracted from the raw recording ready for a machine learning algorthem to process it. While cleaning operation like de-noising or de-reverbing are done. Further, it can be attempted to use multi channel recordings that are done with spatial separated microphone arrays, like this dataset is recorded with 8 microphones in a circle.  The feature could be formulated in the time domain but usually are left in frequency domain so that the output is a form of the spectrum like Welch in 1D or a STFT or alike in 2D. Other outputs are possible like envelopes BSS (blind source separation) de-mixing estimations or DOA (direction of arrival) as well as basic statistics like SNR (sound to noise ratio) estimation or standard deviation etc.

In this study, we settled with:
* MEL spectrum
* Welch spectrum ( called PSD here, even then, even if not it is not the density, but the spectral power V^2 instead of V^2/f)
* FastICA mixing matrix estimation

We also explored other forms find below remarks to that exploration.

For pre-filtering we settled on:
* nn-filter denoising
* FastICA
* K means clustering on STFT to find activation

Further audio augmentation for pseudo supervision is a topic in feature extraction.

In the documentation many links lead to Jupyter notebooks in the the folder feature_extraction_diagrams.


## Diagrams

A feature extraction diagram is a representation of flow diagram that draws the processing steps from the raw input audio towards the output port.
An output port is a spectrum of some kind either 1D or 2D, or some other data like ICA demix matrix. in this study we have mostly used an MEL Spectra and Welch spectra.
While the connection between input port and output port is a path of filters, these filters are drawn out inside the diagram.A feature extraction diagram is a class that consists of the diagram formulated in code and the necessary memory to accumulate multiple processing's off inputs. This helps in maintaining many input files and all the extracted features in memory before writing them to disk. This assists in computational speed as its prohibiting writing out multiple small files - We are using it to process all audio files of one machines ID into one single pickle file.. Also it is possible to have multiple diagrams at the same time this on the other hand helps to distribute the processing for feature extraction throughout multithreading.

The individual diagram classes are deprived from one model and the overloaded functions are only one to initialize and the other for the diagram.

In the picture below of drawing of a diagram is shown by the ellipse is representing an output port and the boxes representing filters or other types of pre-processing this allows to document the code as a visual diagram.

![V0](media_feature_extraction/DiagramV0.png)

The diagram shows very simple version of a feature extraction the document on the left side represents the raw input data. The square with the one represents the amount of channels as there are potentially eight coming from the eight microphones.

## Pre Pre Processing and Time Sliceing or Activation detect

There are also pre pre-processing steps that are not strictly speaking a filter as they manipulate the attention in time. This means that the algorithm tries to automatically determine if the machine is active or not and discard the times of in activity for further filtering and spectra calculation.

![valve](media_feature_extraction/MEL_timeslice_valve.png)

The algorithm used in this study sents the raw data of one channel into PCA and then into a K means neighbor clustering. The naive assumption is that the clustering will only find two cluster one with activation and one without in terms of time frames. This works particularly well when the the recording shows significant changes while activation of the machine is happening this is also very often the case. The study has found that the use of this technique is particularly helpful with the valve as this particularly machine part is only active ends very short times the time wise focus on these activation times helps the classifier or outlier detector to learn better what normal sounds like as it automatically ignores times of inactivity that don't have any information about the machines characteristics. Thereby this preprocessing step can only be used for machines that are active sporadically. The supervision of continuous running machines don't benefit from this.

![slider](media_feature_extraction/MEL_timeslice_slider.png)

The implementation used in the study cut out the activation times and re-append them together to create from a 10 second file with some machine activation a 10 second file full of times with machine activation. This is a workaround that is only used to not break that downstream pipeline that had been constructed around files of the same length in terms of recording time.

## Augmentation

The augmentation of any audio file is done as a pre-step in the feature extraction diagram. The augmentation itself is done by randomly designing FIR filters that represent band passes and eventually shifting the frequencies a.k.a. pitching. This type of augmentation leads to the syntactic abnormal recording for the purpose of pseudo-supervised learning [read more about pseudo-supervised learning](../modeling/pseudo_supervised/pseudo_supervised.md). 


##


## Version of diagrams