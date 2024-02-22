import os
from tkinter import *
from tkinter import filedialog as fd 

root = Tk()


def open_text_file(): 
  
    global f
    
    # Specify the file types 
    filetypes = (('text files', '*.txt'), 
                 ('All files', '*.*')) 
  
    # Show the open file dialog by specifying path 
    f = fd.askopenfile(filetypes=filetypes, 
                       initialdir="D:/Downloads") 
  
    # Insert the text extracted from file in a textfield 
    print(f.name)
  
  
# Create an open file button 
open_button = Button(root, text='Open a File', 
                         command=open_text_file) 
open_button.grid(sticky='w', padx=250, pady=50) 

root.mainloop()

import cv2

import numpy as np

import matplotlib.pyplot as plt


import util


import easyocr

#from sql import mysql_store,mysql_find
from firebase import firebase_store,firebase_find

from mail import send_mail

import datetime

import string


model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')

model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')

class_names_path = os.path.join('.', 'model', 'class.names')


# img_path = 'F:/Projects/Project-II/DATA_SET/car-5.jpg'
img_path = f.name
print(img_path)



with open(class_names_path, 'r') as f:

    class_names = [j[:-1] for j in f.readlines() if len(j) > 2]

    f.close()



net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)





img = cv2.imread(img_path)


H, W, _ = img.shape 

    

blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)




net.setInput(blob)


detections = util.get_outputs(net)



bboxes = []

class_ids = []

scores = []

for detection in detections:

    # [x1, x2, x3, x4, x5, x6, ..., x85]

    bbox = detection[:4]


    xc, yc, w, h = bbox

    bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]


    bbox_confidence = detection[4]


    class_id = np.argmax(detection[5:])

    score = np.amax(detection[5:])

    bboxes.append(bbox)
    class_ids.append(class_id)
    scores.append(score)


bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)



reader = easyocr.Reader(['en'])



def remove(text):
    return text.replace(" ","")


def remove_punctuation(input_string):
    translator = str.maketrans("", "", string.punctuation)

    result = input_string.translate(translator)

    return result


for bbox_, bbox in enumerate(bboxes):

    xc, yc, w, h = bbox

    """

    cv2.putText(img,

                    class_names[class_ids[bbox_]],

                    (int(xc - (w / 2)), int(yc + (h / 2) - 20)),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    7,

                    (0, 255, 0),

                    15)

    """

    license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()


    img = cv2.rectangle(img,

                        (int(xc - (w / 2)), int(yc - (h / 2))),

                        (int(xc + (w / 2)), int(yc + (h / 2))),

                        (0, 255, 0),

                        10)
        

    license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
        

    _, license_plate_thresh = cv2.threshold(license_plate_gray, 64, 255, cv2.THRESH_BINARY)


    output = reader.readtext(license_plate_gray)

    for out in output:

        text_bbox, text, text_score = out
        nospace_text1 = remove(text)
        nospace_text = remove_punctuation(nospace_text1)
        print(nospace_text)


current_datetime = datetime.datetime.now()


# gmailid = mysql_find(nospace_text)
# mysql_store(nospace_text,current_datetime)
gmailid  = firebase_find(nospace_text)
firebase_store(nospace_text,current_datetime,gmailid)


send_mail(gmailid,current_datetime,nospace_text)



'''plt.figure()

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


    plt.figure()

    plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))


    plt.figure()

    plt.imshow(cv2.cvtColor(license_plate_gray, cv2.COLOR_BGR2RGB))


    plt.figure()

    plt.imshow(cv2.cvtColor(license_plate_thresh, cv2.COLOR_BGR2RGB))


    plt.show()
'''
