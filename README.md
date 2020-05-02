# NF_Prj_MIMII_Dataset

## What is this repo about




## Orign the project

### based on the data set from zenodo
https://zenodo.org/record/3384388#.XpNAUpnRYuV

### based on the base line project on gitHub
https://github.com/MIMII-hitachi/mimii_baseline

### The Data Set and Machine parts

This is summery and our intpretion of the information given, on first glance to the data

from the paper () we know the followeing about the machine partst

the dataset contains 4 machine parts and 4 varaints each the data set then has 3 levels of SNR

there is very little details overall given that can be, this is ok since the machine algorthem has it neither and 
and needs to just on sound only without any context know how of what a i.e. pump is. But for us the trainers and bulders of the soultion can be of help to contexturlize the diffcultys for some examples.


10sec

#### SNR and about the noise

Signal to noise ration 

#### Valve

The valves are solenoid https://en.wikipedia.org/wiki/Solenoid_valve

General time beahvioer is sportig

#### pump

The pumps are waterpumps that drain water from a pool and discharge water to the poolcontinuously
extra splashing noise
continues running

the assumtion then centrifugal pump https://en.wikipedia.org/wiki/Centrifugal_pump

#### fan

Discription in the data set:
The fans represent industrial fans, which are used to provide a continuous flow of gas or air in factorie
assumtion is that it will be :Industrial Centrifugal Fans
continus operation.
also not clear is if the microphne is in the air stream
https://en.wikipedia.org/wiki/Centrifugal_fan

#### linear slider
The slide railsin this paper represent linear slide systems, which consist of a mov-ing platform and a stage base
somthing similer to this: https://www.thomsonlinear.com/en/products/linear-motion-systems-products

#### Sensor the microphone
8 micrphone sin cicle of 68mm diameter the divce is called tomago 3: http://www.sifi.co.jp/system/modules/pico/index.php?content_id=39
Tomago is japanes for egg microphon design for confrence table to record all particpends evenly
promotion video https://www.youtube.com/watch?v=8zCsN3hCmLc



## Infrstrucure of apporche 

### overview

feature extraction 
prefilter -> denoise or dereverb -> spectra frames -> file 
(augmentatin)

Training pipline - diffrent model types

Ensamble and time accuamtion to 10sec


### feature extraction

#### diagrams

#### denoise tech

#### source seperation 

#### Spectra

#### basic statistics

#### time rearanging

#### auto detction of types
distingush sportic and continus runnning 

#### multi threading 


### audio augmentaion for unsupervised 

### Modling

#### stochastic outlyer detection

#### auto encoder

#### X

### Ensamble Blending

#### time accumation

#### blender

### results

## appliction notes
the application of a alogrithem like that would be imagnable to be embedded in a smart sensor maybe the training needs 
a cloud server or notebook but the outlyer ensamble would run 




## future work

### feature extraction
DOA
time slicing and rearnge
ICA JAde
derverb 
wavelet spectra freq. following...

basic stat brain storming
- >open ideas sub notebooks


### modeling
pseudo supervised 
CNN and U-net attention maps

### performace for embedding
denoise and convuluton etc... what would be the sample buffer

more threading in extraction and training

diagrams STFT transfer instread of time .

## enviroment and tools

### OS

### GPU support for tensorflow

### yml conda envioerment and jupyter


## Credis and refrences

librosa team 
pyroomacustic 
thanks to hitachi ,,,

### litruture and paper
THe following link is list compiled of all inpirational papaers and helpfull litrure to get into the topic serounding 
link

### web links
the following list contains web sites and youtube links that have been insperational or helpfull to undersand the soroudning topcs
assuming from our base line of data scince with some know how in DSP but not so much audio specic and other helpfull stuff.

### github list
the github list contains all insperation links to source code that have been used or have been helpfull examples
at some point for the soultion thanks to all the creators !









