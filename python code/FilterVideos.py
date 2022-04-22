#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:48:15 2022

@author: fall 2021 video ID ece 590 team and spring 2022 Species ID ece
590 team

Function: Crops given video into smaller images sections and picks
the most quality unique images to analyze.
"""

# RUN THIS CODE FIRST!!!!!!!!!
# !pip install opencv-python
# !pip install google-cloud-vision

import io
import os
import cv2
import glob
import requests
import json
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types
from skimage.metrics import structural_similarity
import imutils

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =" credentials.json"

# %%
# fps of video to frames
fps = 20

# Threshold of frame score
threshold1 = 0.80
threshold2 = 0.9

# Read all videos
path1 = 'input'
# path2 = 'output1'
vidnum = 0
for video in glob.glob(os.path.join(path1, '*.[mM][pP]4')):
    # Path to video file
    vidObj = cv2.VideoCapture(video)

    # Used as counter variable
    count = 0

    # Checks whether frames were extracted
    success = 1

    while success:
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        if not success:
            break

        if count % fps == 0:
            # Saves the frames with num
            num = count
            realcount = count/20
            cv2.imwrite("output1/video" + str(vidnum) +
                        "frame%d.jpg" % realcount, image)

        count += 1

    vidnum += 1

# %% cutes images from video
# Instantiates a client
client = vision.ImageAnnotatorClient()

# Read all frames
path2 = 'output1'
picture_list = []
path_list = []
for frame in glob.glob(os.path.join(path2, '*.jpg')):
    # The name of the image file to annotate
    file_name = os.path.abspath(frame)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Step 1: Remove unqualified frames
    score = 0
    max_score = 0
    max_label = ''
    for label in labels:
        score = label.score
        # We do not need threshold1, can change to threshold2
        # (threshold1 is just for testing purposes)
        if score > threshold1:
            max_score = max(score, max_score)
            # Error is right here (not sure what 2021 team means works fine)
            if max_score == score:
                max_label = label

            # print("Score for " + frame + ": "+ "with "+label.description+ ":"+ str(score))

    if max_score < threshold2:
        os.remove(frame)
        # print("---------DELETED---------")

    else:
        picture_list.append([file_name, max_label.description, max_score])
        path_list.append(file_name)
    # print("---------------------------------------------------------------------")
print("done cutting images from video")

# %% removes duplicate images
index = 0

while (index < len(picture_list)-1 and len(picture_list) > 1):

    score_pic_1 = picture_list[index]
    score_pic_2 = picture_list[index+1]
    pic_1 = cv2.imread(path_list[index])
    pic_2 = cv2.imread(path_list[index+1])
    # Convert the images to grayscale
    grayA = cv2.cvtColor(pic_1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(pic_2, cv2.COLOR_BGR2GRAY)
    # Compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    if (score > 0.75):
        if score_pic_1[2] < score_pic_2[2]:
            os.remove(score_pic_1[0])
            image = path_list[index]
            path_list.remove(image)
            picture_list.remove(score_pic_1)
        else:
            os.remove(score_pic_2[0])
            image = path_list[index+1]
            path_list.remove(image)
            picture_list.remove(score_pic_2)
    else:
        index += 1
print("done filtering duplicate images")
print("please run FilterImages.py")
