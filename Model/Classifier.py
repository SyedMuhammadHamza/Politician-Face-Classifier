# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:54:58 2021

@author: Syed Muhammad Hamza
"""
import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import shutil
import pywt
import os

#link = r'C:\Users\Hamza\Desktop\model\Model\testImages\1.jpg'


def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H
def get_cropped_image_if_2_eyes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color


#cropped_image = get_cropped_image_if_2_eyes(link)
#plt.imshow(cropped_image)

############################### LOADING openCV CASCADE PRETRAINED CLASSSIFIERS  ######################################
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

path_to_data = "./dataset/"
path_to_cr_data = "./dataset/cropped/"

img_dirs = []
for entry in os.scandir(path_to_data):
    if entry.is_dir():
        img_dirs.append(entry.path)
        
if os.path.exists(path_to_cr_data):
     shutil.rmtree(path_to_cr_data)#if folder exist remove it
os.mkdir(path_to_cr_data)
        
cropped_image_dirs = []
politician_file_names_dict = {}

for img_dir in img_dirs:
    politician_name = img_dir.split('/')[-1]
    
    
for img_dir in img_dirs:
    count = 1
    politician_name = img_dir.split('/')[-1]
    print(politician_name)
    
    politician_file_names_dict[politician_name] = [] #politician name is a key and value is alist of pictures
    
    for entry in os.scandir(img_dir):#each image in given politician name directory
        roi_color = get_cropped_image_if_2_eyes(entry.path)
        if roi_color is not None:
            cropped_folder = path_to_cr_data + politician_name
            if not os.path.exists(cropped_folder):
                os.makedirs(cropped_folder)
                cropped_image_dirs.append(cropped_folder)
                print("Generating cropped images in folder: ",cropped_folder)
                
            cropped_file_name = politician_name + str(count) + ".png"
            cropped_file_path = cropped_folder + "/" + cropped_file_name 
            
            cv2.imwrite(cropped_file_path, roi_color)
            politician_file_names_dict[politician_name].append(cropped_file_path)
            count += 1

############################################Wavelet transform#########################################################

politician_file_names_dict = {}
for img_dir in cropped_image_dirs:
    politician_name = img_dir.split('/')[-1]
    file_list = []
    for entry in os.scandir(img_dir):
        file_list.append(entry.path)
    politician_file_names_dict[politician_name] = file_list

#first assigning each class a number before data generation and classification 
            
class_dict = {}
count = 0
for politician_name in politician_file_names_dict().keys():
    class_dict[politician_name] = count
    count = count + 1
class_dict

X, y = [], []
for politician_name, training_files in politician_file_names_dict.items():
    for training_image in training_files:
        img = cv2.imread(training_image)
        if img is None:
            continue
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img,'db1',5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3,1),scalled_img_har.reshape(32*32,1)))
        X.append(combined_img)
        y.append(class_dict[politician_name])
        