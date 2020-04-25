# this is a pseudo package to be used in Jupyter via %run ...
# this file loads all components

# in order to work it must be placed in NF_Prj_MIMII_Dataset\utility\feature_extractor
# and the workspace must have the varaibel BASE_FOLDER this can be a relative path from the notbook perspective
# this code assumes it runs from the jupyter notebooks main pwd


# main imports
import numpy as np
import librosa
import librosa.display
import os
import pickle
import sys
import matplotlib.pyplot as plt
import scipy

def package_file_folder(BASE_FOLDER,filename):
    return os.path.os.path.abspath(BASE_FOLDER+'/utility/feature_extractor/' + filename)
    

# run / load the scripts
## -
fp = package_file_folder(BASE_FOLDER, 'feature_extractor_mother.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'feature_extractor_mel_spectra.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'feature_extractor_psd.py') 
exec(open(fp).read())
