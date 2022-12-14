# -*- coding: utf-8 -*-
"""pro123.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DR2EX1EweQL7giPK5M1Zw_SmL0VHScAh
"""

import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image
import PIL.ImageOps
import os, ssl, time

x = np.load('image.npz')['arr_0']
y = pd.read_csv("labels.csv")["labels"]
print(pd.Series(y).value_counts())
classes = ['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
nclasses = len(classes)

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=9, train_size=3500, test_size=500)
#scaling the features
x_train_scaled = x_train/255.0
x_test_scaled = x_test/255.0

lr = LogisticRegression(solver='saga', multi_class='multinomial').fit(x_train_scaled, y_train)
y_pred = lr.predict(x_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("The accuracy is :- ",accuracy)

cap = cv2.VideoCapture(0)
while True:
   try:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    height,width = gray.shape
    upperleft = (int(width/2 - 56),int(height/2 - 56))
    bottomright = (int(width/2 + 56),int(height/2 + 56))
    cv2.rectangle(gray,upperleft,bottomright,(0,255,0),2)
    roi = gray[upperleft[1]:bottomright[1],upperleft[0]:bottomright[0]]
    impil = Image.fromarray(roi)
    imagebw = impil.convert("L")
    imageresized = imagebw.resize((28,28),Image.NTANTIALIAS)
    imageinverted = PIL.ImageOps.invert(imageresized)
    pixelfilter = 20
    minimumpixel = np.percentile(imageinverted,pixelfilter)
    imagescaled = np.clip(imageinverted - minimumpixel,0,255)
    maxpixel = np.max(imageinverted)
    image_bw_resized_inverted_scaled = np.asarray(image_bw_resized_inverted_scaled)/maxpixel
    test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1,784)
    test_pred = lr.predict(test_sample)
    print("Predicted class is: ", test_pred)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
   except Exception as e:
    pass

cap.release()
cv2.destroyAllWindows()