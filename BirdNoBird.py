#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 12:03:30 2022

@author: amandabreton

Function: Checks if there is the potential for a bird in a sound file.
Use after "SplitAudio.py". Utilizes microfaune to determine bird potential.
"""
# %% Import tools
from microfaune.detection import RNNDetector
import pandas as pd
import argparse
import yaml
import os
import scipy.io.wavfile
# %%
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
folder = configs['foldername']
CSVpath = configs['CSVpath']

# %% getting which files are audio
if os.path.exists(os.path.join(folder, ".DS_Store")):
    os.remove(os.path.join(folder, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

if os.path.exists(os.path.join(CSVpath, "BirdConfidences.csv")):
    os.remove(os.path.join(CSVpath, "BirdConfidences.csv"))
else:
    # print("no audiocsv.csv file")
    pass

for filename in os.listdir(folder):
    if filename.endswith(".WAV"):
        name = os.path.join(folder, filename)
    else:
        nonimagecount = +1
        continue

soundList = [os.path.join(folder, name) for name in os.listdir(folder) if
             os.path.isfile(os.path.join(folder, name))]

# %% Run microfaune
audioPaths = []
confidence = []

for i in range(len(soundList)):
    detector = RNNDetector()
    currentSound = soundList[i]
    global_score, local_score = detector.predict_on_wav(currentSound)
    s, audData = scipy.io.wavfile.read(currentSound)
    audioPaths.append(currentSound)
    confidence.append(global_score)

# %% print to a CSV file to view
df = pd.DataFrame(list(zip(soundList, confidence)),
                  columns=['Audio_Paths', 'Highest_Confidence'])
path = CSVpath + "/BirdConfidences.csv"
df.to_csv(path)
