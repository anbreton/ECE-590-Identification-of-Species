#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:48:15 2022

@author: amandabreton
"""
# %% load packages
import pandas as pd
import argparse
import yaml
import os
import shutil

# %% parsing in information
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
source = configs['source']
CSVpath = configs['CSVpath']
highdestination = configs['highdestination']
lowdestination = configs['lowdestination']

threshold = configs['threshold']
# %% getting the file information
for filename in os.listdir(source):
    if filename.endswith(".WAV"):
        name = os.path.join(source, filename)
    else:
        nonimagecount = +1
        continue

soundList  = []
for filename in os.listdir(source):
    if filename.endswith(".WAV") or filename.endswith(".wav"):
        soundList .append(filename)
    else:
        continue
# %% load up the csv file
df = pd.read_csv(CSVpath, usecols= ['Audio_Name', 'Highest_Confidence'])

# %% sort high and low confidence files into seperate folder

for i in range(len(['Audio_Name'])):
    confidence = float(df['Highest_Confidence'][i][1:-1])
    filename = soundList[i]
    if confidence > threshold:
        shutil.move(source + filename, highdestination+filename)
    else:
        shutil.move(source + filename, lowdestination+filename)
        