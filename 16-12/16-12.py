import cv2
# find cv2 library
# Create a VideoCapture object and read from input file
import shutil
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from datetime import datetime

# video capture
try:
    cap = cv2.VideoCapture(cv2.CAP_V4L2)
    #check if cap is opened

except IOError as e:
    print(e)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
#write video in current directory
import os

counter=1
date=str(datetime.now())
folder_name=date

#start_time = time.time()
#check if new_name already exists
while os.path.exists(folder_name):
    folder_name = folder_name + str(counter)
    counter+=1
os.mkdir(folder_name)
#check if save file already exists
video_name = folder_name+'/video.avi'
out = cv2.VideoWriter(video_name, fourcc, 30.0, (1280, 720))

#start timer

start_time = time.time()

# create main function

x2_list = []
counter_list = []
while True:
    
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    
    ret, frame = cap.read()
    if ret is True:
        out.write(frame)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # write the frame
        q
    #frame = cv2.resize(frame, (1280,720))
    cv2.imshow('Pixels', frame) 
        
    frame = frame[100:500,100:400] #80:600
    # Our operations on the frame come here
    rgb = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # introduce threshold to make image black and white and make the eye more visible
    _, threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    # introduce blur to make the imaqge more clear
    blur = cv2.GaussianBlur(threshold, (7 , 5), 0)
    # introduce dilation to make the image more clear
    kernel = np.ones((5, 5))
   
    rows, cols, _ = frame.shape
    contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # introduce contours to make the image more clear
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    # introduce contours to make the image more clear
     
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        #   introduce contours to make the image more clear
        if x > 300 or x < 50:
            x = 0
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        cv2.line(frame, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        cv2.line(frame, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        
        cv2.circle(frame, (x + int(w / 2), y + int(h / 2)), 2, (0, 0, 255), 2)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)
        #    prints minutes and seconds on video
        string_time = time.strftime("%M:%S", time.gmtime(time.time()-start_time))
        time_stamp = datetime.now().strftime("%d/%m/%y %H:%M:%S ")
        cv2.putText(frame, str(time_stamp)+ str(string_time),(5, 20), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame,'x:' + str(x2) + ' y:' + str(y2), (400, 20), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        x2_list.append(x2)
        counter_list.append(string_time)
        
        break
    
    #x2_list.append(x2)
    
    #string_time = time.strftime("%M:%S", time.gmtime(time.time()-start_time))
    
    # Display the resulting frame
    cv2.imshow('Colour', frame)
    
    
    #cv2.imshow('Grey', gray)
    cv2.imshow('Threshold', threshold)

    if cv2.waitKey(1) & 0xFF == ord('q'):
  
        break
        
x2_g=np.array(counter_list)
y2_g=np.array(x2_list)
df = pd.DataFrame({'x': x2_g,  'y': y2_g})

#save both x and y coordinates in one csv file
    
count=1
file_name = 'list.csv'

    
#add df1 and df2 to csv file with two columns
#df.plot(x='x', y='y', kind = 'line')
df.to_csv(file_name, index=False)
shutil.move(file_name,folder_name)

cap.release()
out.release()
cv2.destroyAllWindows()

