# ECE-590-Identification-of-Species
Repository for ECE 590: Rainforest Engineering/Sp22 XPRIZE Identification of 
Species Team.
Includes Identification tools for Audio and Video

## Table of Contents
* [Technologies](#technologies)
* [Installation](#installation)
* [Audio: General info](#audio-general-info)
* [Audio: Instructions](#instructions-audio)
* [Video: General info](#video-general-info)
* [Video: Instructions](#instructions-video)

## [Technologies](#technologies)
This project is made possible thanks to: 
* Python 3.8.8
* Spyder 4
* microfaune (https://github.com/microfaune/microfaune)
* BirdNet (https://github.com/kahst/BirdNET)
* Laptop provided by Dr. Matrin Brooke (Duke University)

## [Installation](#installation)
1. Install Python on your computer. 
2. Clone this repository onto your computer.
3. Install the following programs onto your computer: 
    * BirdNET (https://github.com/kahst/BirdNET)
      - @phdthesis{kahl2019identifying, title={{Identifying Birds by Sound: 
      Large-scale Acoustic Event Recognition for Avian Activity Monitoring}},
      author={Kahl, Stefan},year={2019},
      school={Chemnitz University of Technology}}
    * Install microfaune (https://github.com/microfaune/microfaune)
      * pip install microfaune-ai
    * Install the following packages if needed using pip install: 
      pandas, os, scipy, pydub, shutil, math, tensorflow (version 2.3.0 ideal),
      pillow, google.cloud, google-cloud-vision, opencv-python, 
      scikit-image opencv-python imutils

## [Audio: General info](#audio-general-info)
The python codes you will need analyzing and sorting audio data from field 
recordings and descriptions of what they do follow below:

* SplitAudio.py: Splits long audio files into one minute (60 seconds) 
* BirdNoBird.py: Goes through a folder fo audio files and determines likelyhood 
  of there being a bird call in it. Outputs the probability to a CSV file. 
* SortConfidences: Moves audio files above a given threshold to a given
  folder, and audio files below threshold to another folder.

## [Audio: Instructions](#instructions-audio)
1. Complete #installation
2. See if statements below:
    * If audio file(s) are longer than desired length, place into folder called 
    "audio_ToSplit". Audio files will be split into 1 minute sections saved as
    .wav files. If you wish for a different duration of time, please edit 
    SplitAudio.py accordingly. 
    * If audio files are desired length into the folder called "audio_input". 
5. Go to terminal and cd into the folder containing the code. 
6. In the terminal type: python SplitAudio.py 
7. In the terminal type: python BirdNoBird.py 
    * Wait til done. You can ignore tensorflow warnings.
8. In the terminal type: python SortConfidences.py
9. To listen to audio files with birds, listen to audio files located in folder
   called "audio_bestbirds". 
    * if you want to listen to things that probably do not contain birds, you can
    by accesing the folder called "audio_nobirds"


## [Video: General info](#video-general-info)
The python codes you will need analyzing and sorting video data from field/drone 
recordings and descriptions of what they do follow below:

* FilterVideos.py: Crops given video into smaller images sections and picks
  the most quality unique images to analyze.
* FilterImages.py: Crops the images gotten from FilterVideos.py to only contain
  the object of interest and sorts them into labeled folders. 
  
## [Video: Instructions](#instructions-video)
1. Complete #installation
2. Place your videos into the folder called "input"
3. Go to terminal and cd into the folder containing the code. 
4. In the terminal type: python FilterVideos.py 
5. In the terminal type: python FilterImages.py 
6. View images if you so desire in: "Labeled Cropped Images"