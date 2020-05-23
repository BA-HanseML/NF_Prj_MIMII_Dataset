# Workflow Improvements

## Environment and portability
A lot can be sad about portability of a python project and this project sure could make use powerful solutions like docker etc. as we encountered some annoying inconstancy’s with conda environments alone and package versions. As well as the general catch up race with tensor flow versions. It is great that everything is progressing fast but for development a frozen base line is important, so that rock solid environment building that might be portable to a cloud is very important to maintain the accessibility of concept study’s and examples as they may be only base to learning of checking if something is worth developing further. We made a effort to make it easy to follow our setup but we also feel that there are better ways to explore.

## File processing and multi-threading
In particular the preprocessing pipeline is suffering with performance problems do to many small files so we countered it with holding a large list in memory and distributed sub lists to threads to increase processing speeds for the feature extraction. But this came with a lot extra effort and we just had no time to get a solid version up and running so the current state is working and fast enough to conduct a study, but must be recoded if this going bigger scale or going to be fully automatized.

## feature extraction performance
many things can be done to feature extraction performance if the middle ground is actually used time frame instead of 10sec that are then chunked or scanned by the spectrum algorithm. One way is to use a STFT as middle ground and do no iFT transformation at all. But do to the experimental nature of the study this was not explored too much.
Further the linear algebra operation on many files could be stacked and sent to the CUDA core on the GPU, some initial experiments with tensor flow STFT function showed promising results but would have been in need of to much recoding for the project time available.

## Jupyter Notebooks – Utility’s- custom library’s and Unit test
IPython notebooks are very powerful if only fully tested packages are used but we also developed heavily utility modules from within a Jupyter notebook and found that this is not a very practical, comparing it to IDE like pyCharm. It is always hard to find the right balance when to move out of the notebook to develop the utility’s in py files. To then reuse the custom library’s in the notebook to explain the analytic path through notebook.
This project created wrappers for sklearn like models and the feature extraction and feature extraction diagram classes that would be better placed in a python model – maybe if time allows this is extracted into its own library including proper unit testing.
