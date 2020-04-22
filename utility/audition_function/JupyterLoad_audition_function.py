# this is a pseudo package to be used in Jupyter via %run ...
# this file loads all components

# in order to work it must be placed in NF_Prj_MIMII_Dataset\utility\audition_function
# and the workspace must have the varaibel BASE_FOLDER this can be a relative path from the notbook perspective
# this code assumes it runs from the jupyter notebooks main pwd


# main imports

import numpy as np
import pandas as pd
import os
from IPython.display import display, Markdown, Audio
import librosa
import librosa.display
import matplotlib.cm as cm


def package_file_folder(BASE_FOLDER,filename):
    return os.path.os.path.abspath(BASE_FOLDER+'/utility/audition_function/' + filename)
    

# run / load the scripts
## -
fp = package_file_folder(BASE_FOLDER, 'audition_function_main.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'audition_function_audio.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'audition_function_baseplots.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'audition_function_akkuplot.py') 
exec(open(fp).read())