# Pseudo supervised 
Learning on synthetic abnormal constructed in the feature extraction by augmenting the normal with random distortions.
## Exploration approaches Step 1
In Step 1 all notebooks in this folder with a prefix “S01” an exploration of classic machine learning algorithms is done and some spot checks through out the possible machines and noise level.
In this step some conclusion can be made:
* all algorithm fitting very well in training (this means the synthetic abnormal are in way to easy to distinguish)
* if the augmentation is not in feed back with the training exploration of more advanced algorithms like boosting or neural networks will not be able to create better results
* the augmentation form that is chosen right now is distorting the spectra over all time frames so that the 1d spectra are dominate feature.
* Random Forest and Support vector machine are most promising over all
## Full training of the top Step 2
In Step 2 all notebooks in the folder with a prefix of “S02” that deal with training and summery of the two sets the design set ID00 and ID02 and the validation set ID04 and ID06
Conclusion in this step
* the approaches is promising as it can beat the auto encoder from the base line
* it is worth splitting the machines by activation type as different algorithm seem to fit better depending on the type – this all is based on combination of augmentation feat. Extraction and ML algorithm and might change if any part of the chain is changed
* the most promising combination is PSD_raw into a SVM for sporadic activated machines.
