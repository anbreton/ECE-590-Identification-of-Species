#RUN THIS FIRST!!!!!!!!!
!pip install opencv-python
!pip install google-cloud-vision
import io
import os
import cv2
import glob
import requests
import json


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ocean-engineering-96e0c62d5fe3.json"
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types


def distanceCalc(pic_1,pic_2):
    r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        files={
            'image1': open(pic_1, 'rb'),
            'image2': open(pic_2, 'rb'),
        },
        headers={'api-key': '7e7d3b99-2106-4b27-9ef4-9e3e2fccf04b'} #NEED A UNIQUE API KEY!!!!!!!!!!!!!!!!!!!
        )
    distanceDict = r.json()
    
    distance = distanceDict['output']["distance"]
    distance = int(distance)
    
    
    return distance

# fps of video to frames
fps = 20

# Threshold of frame score
threshold1 = 0.80
threshold2 = 0.9

# Read all videos
path1 = 'input'
#path2 = 'output1'
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

# Instantiates a client
client = vision.ImageAnnotatorClient()

# Read all frames
path2 = 'output1'
picture_list = []
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
        #We do not need threshold1, can change to threshold2 (threshold1 is just for testing purposes)
        if score > threshold1:
            max_score = max(score,max_score)
            #Error is right here
            if max_score == score:
                max_label = label
            
            print("Score for " + frame + ": "+ "with "+label.description+ ":"+ str(score))
        
    if max_score < threshold2:
        os.remove(frame)
        print("---------DELETED---------")

    else:
        picture_list.append([file_name, max_label.description, max_score])
    print("---------------------------------------------------------------------")
    
#We want to delete if similarity checker returns value greater than 30 and top label is the same
#Step 2: Checks similarity of two images to each other



index = 0

while (index < len(picture_list)-1 and len(picture_list) > 1):
    
    pic_1 = picture_list[index]
    pic_2 = picture_list[index+1]
    print(pic_1[1])
    print(pic_1[2])
    print(pic_2[1])
    print(pic_2[2])
    distance = distanceCalc(pic_1[0],pic_2[0])

    
    if (distance <=20 and (pic_1[1] == pic_2[1])) :
        print("Deleting Image")
        if pic_1[2] < pic_2[2]:
            os.remove(pic_1[0])
            picture_list.remove(pic_1)
        else:
            os.remove(pic_2[0])
            picture_list.remove(pic_2)
    else:
        index += 1
        
            
        

