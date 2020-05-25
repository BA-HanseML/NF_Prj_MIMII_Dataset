# Dataset MIMII

[Main Source](https://zenodo.org/record/3384388#.XpNAUpnRYuV)

## general

Best discription is given in the [paper](https://arxiv.org/pdf/1909.09347.pdf) from Research and Development Group at Hitachi, Ltd

The dataset downloaded form the [zenodo MIMII](https://zenodo.org/record/3384388#.XpNAUpnRYuV) has recordings of 4 machine parts each comes as 4 types named as ID00, ID02, ID04 and ID06. The even numbers from the paper are not available.
Recordings are done in 16kHz with a 8 channel the used microphone is [TAMAGO-03 microphone](http://www.sifi.co.jp/system/modules/pico/index.php?content_id=39) from [System In Frontier Inc](http://www.sifi.co.jp/en/)

## noise level

the noise is added after the recording of the machines but the noise is recorded in a real environments so the nature of noise is realistic and do to the separated while recording the noise to signal ratio could be adjusted by the creators. The data set comes only with noise polluted recordings in 3 levels of SNR.

## show room 
if you like to get a feeling for what the recordings are
check out the show room at https://ba-hanseml.github.io/MIMII_show_room/showroom.html

to look at spectra and liston to mono mp3 of some recordings in high noise -6dB of SNR.

## The machines parts

namely there are 4: 
* pump
* valve
* rail slider
* fan

Unfortunately, not too much information is given but it can be deducted from sound sample and the paper that 

**Pumps** are likely small to midsize centrifugal pumps that pump water.

The **valves** are solenoid valves of various sizes.

The **rail slider** is most likely an actively driven motorized positioning rails slider more commonly called linear motion systems.

**Fans** are described as: “The fans represent industrial fans, which are used to provide a continuous flow of gas or air in factories” This indicates medium to large size centrifugal fans.

Some more intuition can be found from links in the [refrences](../ref/web_list.md)






