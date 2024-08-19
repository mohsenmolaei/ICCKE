# -*- coding: utf-8 -*-
"""yolo5m.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10FY4-nxYSljrDPNDW_BuKoAFwifQ5S2H
"""

from google.colab import drive
drive.mount('/content/drive')

pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
import cv2
!pip install roboflow
from roboflow import Roboflow
import torch
from datetime import datetime

!git clone https://github.com/ultralytics/yolov5  # clone repo
# %cd yolov5

rf = Roboflow(api_key="*******")
project = rf.workspace("nena-trikic-ljxt3").project("tensorflowrecords")
dataset = project.version(5).download("yolov5")

# Commented out IPython magic to ensure Python compatibility.
# %mkdir {dataset.location}/valid
# %mkdir {dataset.location}/valid/images
# %mkdir {dataset.location}/valid/labels
# %mv {dataset.location}/train/images/0---Copy_png.rf.ac81468eb7a79f0c6ef0610303c9a663.jpg {dataset.location}/valid/images
# %mv {dataset.location}/train/labels/0---Copy_png.rf.ac81468eb7a79f0c6ef0610303c9a663.txt {dataset.location}/valid/labels
dataset.location

!python ./train.py --img 416 --batch 16 --epochs 150 --data {dataset.location}/data.yaml  --weights yolov5s.pt --cache

# !python detect.py --source "/content/drive/MyDrive/Train/4.mp4" --weights "/content/drive/MyDrive/best.pt"

# Commented out IPython magic to ensure Python compatibility.

# %rm -R '/content/output_detection'
# %mkdir '/content/output_detection'
# %cd '/content/output_detection'
#Video file Or Camera device
cap= cv2.VideoCapture('/content/drive/MyDrive/Train/8.mp4')

model_name='/content/drive/MyDrive/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True) 

i=0
imgOld = []
#realTime  Read frame
diffVectors = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i % 1 == 0 :
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        if    int(current_time[-2:]) % 3 == 0 :
            results = model(frame)
            cv2.imwrite('./output_detection/'+str(current_time)+'.jpg',results.render()[0])
            print("chickens: " ,len(results.pandas().xyxy[0]))
    i+=1

