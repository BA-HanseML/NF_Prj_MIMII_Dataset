# this is a pseudo package to be used in Jupyter via %run ...
# this file loads all components

# in order to work it must be placed in NF_Prj_MIMII_Dataset\utility\modeling
# and the workspace must have the varaibel BASE_FOLDER this can be a relative path from the notbook perspective
# this code assumes it runs from the jupyter notebooks main pwd


# main imports
import numpy as np
import pandas as pd
#import librosa
#import librosa.display
import os
import pickle
#import sys
import matplotlib.pyplot as plt
from tqdm import tqdm

from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score
from sklearn.model_selection import train_test_split

import scipy
from scipy.signal import argrelextrema

def package_file_folder(BASE_FOLDER,filename):
    return os.path.os.path.abspath(BASE_FOLDER+'/utility/modeling/' + filename)
    
# run / load the scripts
## -
fp = package_file_folder(BASE_FOLDER, 'load_data.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'split_data.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'clustering.py') 
exec(open(fp).read())