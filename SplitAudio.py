#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 11:22:59 2022

@author: amandabreton

Function: Splits audio into smaller sections
"""
from pydub import AudioSegment
import math
import argparse
import yaml
import shutil
import os 

parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
folder = configs['foldername']
source = folder
#file = configs['filename']
duration = configs['lengthofsplit']  # length in min
destination = configs['analyzefolder']
# Mac/Linux use: '/'
# Windows use: '\\''


class SplitWavAudioMubin():
    """Function: Splits audio into smaller sections."""

    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename
        self.audio = AudioSegment.from_wav(self.filepath)
        self.destination = destination
        self.source = source

    def get_duration(self):
        """Get the duration of the audio file."""
        return self.audio.duration_seconds

    def single_split(self, from_min, to_min, split_filename):
        """Perform single split on file."""
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '/' + split_filename, format="wav")

    def multiple_split(self, min_per_split):
        """Perform multiple splits on file."""
        total_mins = math.ceil(self.get_duration() / 60)
        audioList = []
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            audioList.append(split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')
                for f in audioList:
                    shutil.move(self.source + f, self.destination + f)


# %% Getting the file names
if os.path.exists(os.path.join(folder, ".DS_Store")):
    os.remove(os.path.join(folder, ".DS_Store"))
else:
    pass
audioList = []
for filename in os.listdir(folder):
    if filename.endswith(".WAV"):
        audioList.append(filename)
        print(filename)
    else:
        nonimagecount = +1
        continue
# %% Splitting execution
for i in range(len(audioList)):
    file = audioList[i]
    split_wav = SplitWavAudioMubin(folder, file)
    split_wav.multiple_split(min_per_split=duration)
