#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:48:15 2022

@author: amandabreton

Function: Crops the images gotten from FilterVideos.py to only contain
the object of interest and sorts them into labeled folders.
"""
# !pip install pillow
# !pip install google.cloud
# !pip install google-cloud-vision

# %%
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

from google.cloud import vision

import PIL 

import io
import os
import cv2
import glob
import random

from PIL import Image, ImageDraw, Image, ImageFont
import pandas as pd

# %%
def createCroppedImage(pillow_image, bounding, image_size, i,  caption='', confidence_score=0):
    global countImages
    width, height = image_size
    if confidence_score >= 0.85:
        # print(width, height)
        # print('x0',bounding.normalized_vertices[0].x * width)
        # print('y0',bounding.normalized_vertices[0].y * height)

        # print('x1',bounding.normalized_vertices[1].x * width)
        # print('y1',bounding.normalized_vertices[1].y * height)

        # print('x2',bounding.normalized_vertices[2].x * width)
        # print('y2',bounding.normalized_vertices[2].y * height)

        # print('x3',bounding.normalized_vertices[3].x * width)
        # print('y3',bounding.normalized_vertices[3].y * height)

        area = (bounding.normalized_vertices[0].x * width,
                bounding.normalized_vertices[0].y * height,
                bounding.normalized_vertices[2].x * width,
                bounding.normalized_vertices[2].y * height)
        cropped_img = pillow_image.crop(area)
        pathCaption = 'Labeled Cropped Images/'+caption+'/'

        if not os.path.isdir(pathCaption):
            os.mkdir(pathCaption)
            countImages[caption] = 0

        #print(pathCaption+caption+'_'+str(countImages[caption])+'.png')

        cropped_img.save(pathCaption+caption+'_'+str(countImages[caption])+'.png')

        countImages[caption] += 1


def draw_borders(pillow_image, bounding, color, image_size, caption='', confidence_score=0):

    width, height = image_size
    draw = ImageDraw.Draw(pillow_image)
    draw.polygon([
        bounding.normalized_vertices[0].x *
        width, bounding.normalized_vertices[0].y * height,
        bounding.normalized_vertices[1].x *
        width, bounding.normalized_vertices[1].y * height,
        bounding.normalized_vertices[2].x *
        width, bounding.normalized_vertices[2].y * height,
        bounding.normalized_vertices[3].x * width,
        bounding.normalized_vertices[3].y * height], fill=None, outline=color)

    # TODO: Validation needed
    font_size = width * height // 22000 if width * height > 400000 else 12

    # font = ImageFont.truetype(r'C:/Users/jiejenn/AppData/Local/Microsoft/Windows/Fonts/opensans-regular.ttf', 22)

    draw.text((bounding.normalized_vertices[0].x * width,
               bounding.normalized_vertices[0].y * height), text=caption, fill=color)

    # insert confidence score
    draw.text((bounding.normalized_vertices[0].x * width, bounding.normalized_vertices[0].y *
               height + 20), text='Confidence Score: {0:.2f}%'.format(confidence_score), fill=color)

    return pillow_image

# %%
def draw_boundaries(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    pillow_image = Image.open(path)
    df = pd.DataFrame(columns=['name', 'score'])

    print('Number of objects found: {}'.format(len(objects)))
    i = 0

    for obj in objects:
        createCroppedImage(pillow_image, obj.bounding_poly, pillow_image.size, i, obj.name, obj.score)
        i+= 1
    for object_ in objects:
        #print('\n{} (confidence: {})'.format(object_.name, object_.score))
        #print('Normalized bounding polygon vertices: ')

        df = df.append(dict(name=object_.name, score=object_.score),ignore_index=True)

        r, g, b = random.randint(150, 255), random.randint(150, 255),
        random.randint(150, 255)

        draw_borders(pillow_image, object_.bounding_poly, (r, g, b),
                     pillow_image.size, object_.name, object_.score)

        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    # print(df)
    pillow_image


# %%
inputPath = 'output1'
countImages = {}
for f in os.listdir(inputPath):
    if (f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.jpg')):
        draw_boundaries(os.path.join(inputPath, f))

print('Done you may view images now :)')
print('Done')
