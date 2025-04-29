import pickle
import cv2
import cvzone
import numpy as np 

cap =cv2.VideoCapture('D:/car-parking/carPark (1) (1).mp4')

with open ('carparkpoition','rb') as f:
        posList = pickle.load(f)

width , height = 107, 48

def checkParkingspace(imgpro):
     
     spacecounter = 0
     for pos in posList:
        x,y = pos

        imgCrop = imgpro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count <850:
             color = (0,255,0)
             thickness = 5
             spacecounter +=1
        else:
             color = (0,0,255)
             thickness = 2
        cv2.rectangle(img,pos,(pos[0] + width,pos[1] + height),color,thickness)
        cvzone.putTextRect(img, f'Free : {spacecounter}/{len(posList)}',(100,50),scale=3,thickness=5,offset=20,colorR=(0,200,0))





while True :

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imggray,(3,3),1)
    imgthreshold = cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgmedian =cv2.medianBlur(imgthreshold,5)
    kernel = np.ones((3,3), np.uint8)
    imgdilate = cv2.dilate(imgmedian,kernel, iterations=1)


    checkParkingspace(imgdilate)
    

    cv2.imshow('image',img)
    cv2.imshow('image-blur',imgblur)
    cv2.imshow('image-threshold',imgthreshold)
    cv2.imshow('image-median',imgmedian)



    if cv2.waitKey(10) & 0xff==ord('q'):
        break