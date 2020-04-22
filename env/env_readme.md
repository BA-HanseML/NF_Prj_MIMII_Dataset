# cooperational guidline

Main enviorment name = 
Main enviorment jupyter dispaly name =
GPU post fix

dataset extention

rules for utiltys



# Baseline dependencys

## orginal list
keras==2.1.6
Keras-Applications==1.0.8
Keras-Preprocessing==1.0.5

matplotlib==3.0.3
numpy==1.16.0
PyYAML==5.1
scikit-learn==0.20.2
librosa==0.6.0
audioread==2.1.5
setuptools==41.0.0
tensorflow==1.15.0

## Tensor Flow Win10 CUDA
check if GPU is CUDA compatible : https://developer.nvidia.com/cuda-gpus
Arne : GeForce GTX 970 Compute Capability = 5.2

## find out what version of driver is installed
Open Control Panel.
Click on Hardware and Sound.
Click on NVIDIA Control Panel.
Click the System Information option from the bottom-left corner.
Arne : GeForce GTX 970 V 416.6 CUDA cores 1664 - 4 GB GDDR5



Read out based on https://www.youtube.com/watch?v=qrkEYf-YDyI
* TensorFlow veraion is linked to CUDA version driver of nvidia
* order is importent
### Step 1
identify GPU !! : Deivice Manager -> Display reads (NVIDIA GeForce GTX 970)

### Step 2 Driver find !

https://www.tensorflow.org/install/gpu
-> notice that only Tesla Driver come with preincluded Cuda!!!!
-> get cuda toolkit https://developer.nvidia.com/cuda-downloads
-> or more specific cuda toolkit by verison https://developer.nvidia.com/cuda-toolkit-archive
- While installing the toolkit make sure that you install the CUPTI ...
- for cuDNN you need a NVIDA dev accound then the link is https://developer.nvidia.com/rdp/cudnn-download

??! What is it with Visual Studio support
https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&rel=16
in cuda 10 you need vs2015 / VS2017 !s


**For TF 2.0 / 1.15**
NVIDIA® GPU drivers —CUDA 10.0 requires 410.x or higher.
CUDA® Toolkit —TensorFlow supports CUDA 10.0 (TensorFlow >= 1.13.0)
CUPTI ships with the CUDA Toolkit.
cuDNN SDK (>= 7.4.1)
(TensorRT 5.0)

**For TF 2.1...**
NVIDIA® GPU drivers —CUDA 10.1 requires 418.x or higher.
CUDA® Toolkit —TensorFlow supports CUDA 10.1 (TensorFlow >= 2.1.0)
CUPTI ships with the CUDA Toolkit.
cuDNN SDK (>= 7.6)
 (TensorRT 6.0)

### Step 2.5 ( seems optional)
install VS 2015 or 2017

### Step 3 Install in the right order

### Step 4 install cuDNN
copy file form zip to c:\tools

### Step 5 add enviroment paths
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\extras\CUPTI\libx64
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\include
* C:\tools\cuda\bin

### Step 5.1 ( seems optional = Install TensorRT
Download the GA version fitting to CUDA version i.e. 10.0
copy to the c:\tools
add path to the root of tje TensorRT

### Suggestion wiht Miniconda
...

### YML design best guess:

check Keras 2.1.6  https://github.com/keras-team/keras/releases/tag/2.1.6
is based on TensorFLow 1.15 ...
- > I would say give it a shot with 2.0

name: mimii_tf2
 
dependencies:
    - python=3.7
    - pip>=19.0
    - jupyter
    - tensorflow-gpu=2.0
    - scikit-learn
    - scipy
    - pandas
    - pandas-datareader
    - matplotlib
    - tqdm
    - pyyaml
	- setuptools
	- numpy
	- audioread
	- keras
	- Keras-Applications
	- Keras-Preprocessing




## env pip/conda commands

### install by hand
#### librosa
conda install -c conda-forge librosa
#### ffmpeg
conda install -c conda-forge ffmpeg
#### audioread
audioread == 2.1.5 (more)
conda install -c conda-forge audioread

#### TODO experiment with conda channels


### export yml
conda env export  > _full_export.yml
conda env export --no-builds > _full_nb_export.yml

### Install the env
conda env create -f env2.yml



### install to jupyter
python -m ipykernel install --user --name testTF2p1 --display-name "Py3.7 (TF1)"

### install jupyter extention
#### S1 install
conda install -c conda-forge jupyter_contrib_nbextensions
#### S2 Java CSS etc
jupyter contrib nbextension install --user

# env backup 


# Docker Windows Host and V-Linux
download docker for windows
https://hub.docker.com/editions/community/docker-ce-desktop-windows

https://www.tensorflow.org/install/docker

# Orecal VM Box Windows Host - Ubunto GPU support