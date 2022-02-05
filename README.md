# ECE-590-Identification-of-Species
Repository for ECE 590: Rainforest Engineering/Sp22 XPRIZE Identification of Species Team

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Instructions](#instructions)

## General info
This project contains various python codes used for analyzing and sorting audio
data from field recordings. Files include: 

* SplitAudio.py: Splits long audio files into one minute (60 seconds) 
* BirdNoBird.py: Goes through a folder fo audio files and determines likelyhood 
  of there being a bird call in it. Outputs the probability to a CSV file. 
  
## [Technologies](#technologies)
Project is created with: 
* Python 3.8.8
* Spyder 4
* microfaune (https://github.com/microfaune/microfaune)

## [Setup](#setup)

* SplitAudio.py:
    1. Open SplitAudio.yaml file and edit to have paths to the folder containing the 
    audio files to split and folder for a destination for the split audio files. 
          Example of yaml file: 
          foldername: "/Users/amandabreton/Desktop/ECE590/AudioFiles_ToSplit/"
          lengthofsplit: 1
          analyzefolder: "/Users/amandabreton/Desktop/ECE590/AudioFiles_ToAnalyze/"

* BirdNoBird.py:
    1. Open BirdNoBird.yaml file and edit to have paths to the folder containing the 
    split audio files a folder for a destination for CSV file output. 
      Example of yaml file: 
      foldername: "/Users/amandabreton/Desktop/ECE590/AudioFiles_ToAnalyze"
      CSVpath: "/Users/amandabreton/Desktop/ECE590"

*  SortConfidences.py: 
    1. Open SortConfidences.yaml file and edit to have the desired threshold as
    a cut off. Also edit to have paths of the analyzed audio files and where you
    want the files with high/low confidence. 
      Example of yaml file:
      CSVpath: "/Users/amandabreton/Desktop/BirdConfidences.csv"
      source: "/Users/amandabreton/Desktop/ECE590/AudioFiles_DoneAnalyzing/"
      highdestination: "/Users/amandabreton/Desktop/ECE590/HighConfidence/"
      lowdestination: "/Users/amandabreton/Desktop/ECE590/LowConfidence/"
      threshold: 0.5


## [Instructions](#instructions)

1. Install Python on computer. 
2. Install microfaune (https://github.com/microfaune/microfaune) and any other 
  packages you may need such as: pandas, argparse, yaml, os, scipy, pydub, 
  shutil, math, and tensorflow (version 2.3.0 ideal). 
3. Create folders for: 
    * source of audio file(s), ideally: "AudioFiles_ToSplit""
    * destination folder for split audio files ideally: "AudioFiles_ToAnalyze"
    * destination folder for analyzed files ideally: "AudioFiles_DoneAnalyzing"
    * folder for high confidence files ideally: "HighConfidence"
    * folder for low confidence files ideally: "LowConfidence"
4. See and do #setup 
5. Go to terminal and cd into the folder containing the code. 
6. In the terminal type: python SplitAudio.py SplitAudio.yaml
7. In the terminal type: python BirdNoBird.py BirdNoBird.yaml
8. Wait til done. You can ignore tensorflow warnings. 
9. In the terminal type: python SortConfidences.py SortConfidences.yaml 