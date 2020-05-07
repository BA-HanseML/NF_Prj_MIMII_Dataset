# this is a pseudo package to be used in Jupyter via %run ...
# this file loads all components

# in order to work it must be placed in NF_Prj_MIMII_Dataset\utility\modeling
# and the workspace must have the varaibel BASE_FOLDER this can be a relative path from the notbook perspective
# this code assumes it runs from the jupyter notebooks main pwd

import os

def package_file_folder(BASE_FOLDER,filename):
    return os.path.os.path.abspath(BASE_FOLDER+'/utility/modeling/' + filename)

# import/load all subscripts
## -
fp = package_file_folder(BASE_FOLDER, 'load_data.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'split_data.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'anomaly_detection_models.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'pseudo_supervised_models.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'ann_models.py') 
exec(open(fp).read())
## -
fp = package_file_folder(BASE_FOLDER, 'detection_pipe.py') 
exec(open(fp).read())