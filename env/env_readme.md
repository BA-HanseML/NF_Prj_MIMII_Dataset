# Environments Notes


Environment parameter is important to know if the code is reused. So here a collection to the topics:

* Conda environment
* Jupyter
* Python packages
* OS 
* GPU CUDA support

## OS
The work was done on Windows 10.

## Conda environment 
Find the enviromet yml files in the sub folder for the OS as different favors

* With and without GPU
* Fully exported with built version and without
* Hand written env. that just name the main packages

We noticed when reproducing environments that all the versions are not as portable as wished between systems therefore we added all the flavors in the hope it assists in reproducing the environment if trouble arise the best go to file is:
env_baseline_withGPU_TF2.yml
It will create the environment: mimiibaseTF2GPU

### conda most important commands

### exporting
```
conda env export  > _full_export.yml
conda env export --no-builds > _full_nb_export.yml
```

### install/ create
```
conda env create -f env_baseline_withGPU_TF2.yml
```

## Jupyter
Jupyter notebooks need a mapping name for environments over time, many of these environments mappings are stashing up so we used on common one for this project:

* Py3.7 (mimii_base_TF2_GPU)
* Py3.7 (mimii_base_TF2)

### Jupyter to Conda env. on Windows
On windows it seems necessary to connect the environment with the following command to Jupiter:
```
python -m ipykernel install --user --name testTF2p1 --display-name "Py3.7 (mimii_base_TF2_GPU)"
```

### Jupyter extention
We found the extention very helpfull thanks to the creators !
```
conda install -c conda-forge jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

## Python packages 
Find them listed in the environment [env_baseline_withGPU_TF2.yml](windows_10/env_baseline_withGPU_TF2.yml)

Some packages may install better by hand we had this experience but this does not have to be necessary:

### librosa
```
conda install -c conda-forge librosa
```
### ffmpeg
```
conda install -c conda-forge ffmpeg
```
### audioread

audioread == 2.1.5 (more)
```
conda install -c conda-forge audioread
```

## GPU - CONDA and Tensorflow - Windows

To install tensor flow for windows we followed the awsom instruction form Jeff Heaton: https://www.youtube.com/watch?v=qrkEYf-YDyI

### General steps
Check if GPU is CUDA compatible : https://developer.nvidia.com/cuda-gpus

#### Find out what version of driver is installed
Open Control Panel.
Click on Hardware and Sound.
Click on NVIDIA Control Panel.
Click the System Information option from the bottom-left corner.

example find: GeForce GTX 970 V 416.6 CUDA cores 1664 - 4 GB GDDR5

#### install Visual Studio
For cuda 10 you need VS2015 / VS2017 !s

#### Find the driver
-> notice that only Tesla Driver come with preincluded Cuda!!!!
-> get cuda toolkit https://developer.nvidia.com/cuda-downloads
-> or more specific cuda toolkit by verison https://developer.nvidia.com/cuda-toolkit-archive
- While installing the toolkit make sure that you install the CUPTI ...
- for cuDNN you need a NVIDA dev accound then the link is https://developer.nvidia.com/rdp/cudnn-download

Versions:
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

#### Install CuDNN
Copy file from zip to c:\tools

Add following to PATH of your system:
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\extras\CUPTI\libx64
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\include
* C:\tools\cuda\bin

#### Tensor RT
Download the GA version fitting to CUDA version, i.e. 10.0
Copy to the c:\tools
add path to the root of the TensorRT folder


add path to the root of tje TensorRT

