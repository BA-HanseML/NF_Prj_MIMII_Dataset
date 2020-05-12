# Main folder level 0
* 0dB
* 6dB
* min6dB

## sub folder level 1 = machine part class
* 0dB/fan
* 0dB/pump
* 0dB/slider
* 0dB/valve

## sub folder leve 2 = machine part id
the id is a machine varaint of that class liek pump of type 1 and pump of type 2.
* 0dB/fan/id_00
* 0dB/fan/id_01
* ...
## sub folder leve 3 = label
* 0dB/fan/id_00/abnormal
* 0dB/fan/id_00/normal
instite this folder 8channel  wav files are expected numbered: 00000000.wav

# Auto unpack
## SH script from base line repo 
https://github.com/MIMII-hitachi/mimii_baseline

```
#!bin/sh
mkdir ./min6dB
mkdir ./0dB
mkdir ./6dB
7z -omin6dB -y x ./-6_dB_fan.zip
7z -omin6dB -y x ./-6_dB_valve.zip
7z -omin6dB -y x ./-6_dB_pump.zip
7z -omin6dB -y x ./-6_dB_slider.zip
7z -o6dB -y x ./6_dB_fan.zip
7z -o6dB -y x ./6_dB_valve.zip
7z -o6dB -y x ./6_dB_pump.zip
7z -o6dB -y x ./6_dB_slider.zip
7z -o0dB -y x ./0_dB_fan.zip
7z -o0dB -y x ./0_dB_pump.zip
7z -o0dB -y x ./0_dB_valve.zip
7z -o0dB -y x ./0_dB_slider.zip
```
## batch script 
```
md min6dB
md 0dB
md 6dB
7z.exe -omin6dB -y x .\-6_dB_fan.zip
7z.exe -omin6dB -y x .\-6_dB_valve.zip
7z.exe -omin6dB -y x .\-6_dB_pump.zip
7z.exe -omin6dB -y x .\-6_dB_slider.zip
7z.exe -o6dB -y x .\6_dB_fan.zip
7z.exe -o6dB -y x .\6_dB_valve.zip
7z.exe -o6dB -y x .\6_dB_pump.zip
7z.exe -o6dB -y x .\6_dB_slider.zip
7z.exe -o0dB -y x .\0_dB_fan.zip
7z.exe -o0dB -y x .\0_dB_pump.zip
7z.exe -o0dB -y x .\0_dB_valve.zip
7z.exe -o0dB -y x .\0_dB_slider.zip
```

# Addtional Folders from feature extractrion
Feature extraction will create folder named after the extraction diagram like:
exdia_v1 - for feature extraction diagram version 1 find more about feature extraction diagrams in [feature extraction](../doc/feature_extraction.md)