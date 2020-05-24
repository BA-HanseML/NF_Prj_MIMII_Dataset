# Modeling Overlook

In general the prediction task is the detection of anomalous sound of industrial machine in an unsupervised manner. In the training phase only normal operation sounds are being considered, whereas we try to predict anomalous sound in the evaluation phase. 

The main challenge in the modeling process is to explore the vast space of model permutations and to pick the best models for certain features and combine them to an ensemble. This selection process is segmented:

+ First we are going to take a look at possible preprocessing steps like PCA and ICA. 

+ Second we will create a set of model permutations to explore the effect of different feature-types, model-types and hyperparameters.

+ Third we select the most promising permutations from the subset we created. From those we will build our final ensemble.

# Metric

The ROC AUC is the main metric to compare different models, feature types, etc.

# Preprocessing

## ICA & PCA

[Notebook](./../modeling/preprocessing/preprocessing_exploration.ipynb)

# Model Types

The Modeling part was approached from two perspectives. We followed a pure unsupervised approach with the stochastic and Autoencoder models and a pseudo-supervised approach by data augmentation following a classification.

## Stochastic

Within the unsupervised approach we used two model types for anomaly detection. The stochastic approach makes use of models like:

+ Isolation Forest
+ Elliptic Envelope
+ Gaussian Mixture Model

which assume that the normal operation data belongs to a multi-dimensional distribution. These models are being trained to fit a model-specific representation of this distribution. After that the model is able to calculate whether a new instance can be reproduced from that distribution. The assumption is, that anomalous operation sound is significantly different from and can not be represented by the fitted distribution of normal operation sounds. Depending on the model for each evaluation instance a score or likelihood can be calculated that this instance belongs to the fitted distribution. This score or likelihood is being used as the prediction and from this the area under the curve of the receiver operating characteristic (ROC AUC) is being calculated. 

## Auto-Encoder

The second model type in the unsupervised approach is the Autoencoder. The Autoencoder is a type of artificial neural network specifically designed to learn a lower-dimensional representation of data. The network usually consists of a reduction side, called the Encoder, and a reconstruction side, called the Decoder. In a forward step the data is being "forced" into a lower dimensional form by the Encoder and transformed back into the original dimension by the Decoder. This results in a "condensed" representation of the original data and a reduction of noise. While training the metric is the reconstruction error between the input data and the decoded output data.

![](https://miro.medium.com/max/1400/0*uq2_ZipB9TqI9G_k)
*Example of an Autoencoder, embedded from: https://miro.medium.com/max/1400/0\*uq2_ZipB9TqI9G_k

## Pseudo supervised

The approaches uses supervised machine learning on a set of normal observation and normal augmented, the normal augmented then become synthetic abnormal observation.
[more details](../modeling/pseudo_supervised/pseudo_supervised.md)

# Ensemble

There is a high degree of freedom of different features, preprocessing steps, models, and hyperparameters. Possible permutations consist of 2 signal to noise ratios (SNR), 4 machines each SNR, 2 IDs each machine, 9 different feature-types each ID, results in 144 different permutations to explore before any selection of feature-parameter, model type or model-parameter.

Over all SNRs, machines, IDs, features we trained a set of different models with varying hyperparameters. The set of models will not completely be reproducable but the 

# Results

# References

[[1]](https://www.semanticscholar.org/paper/Detection-of-Abnormal-Sound-Using-Multi-stage-GMM-Ito-Aiba/27628c9aeecb4df6010693533ad79f4d03c64f86) Ito, Akinori, Akihito Aiba, Masashi Ito and Shozo Makino. “Detection of Abnormal Sound Using Multi-stage GMM for Surveillance Microphone.” 2009 Fifth International Conference on Information Assurance and Security 1 (2009): 733-736.