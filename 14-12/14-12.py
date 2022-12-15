import cv2
# find cv2 library
# Create a VideoCapture object and read from input file

import pandas as pd
import numpy as np
import time

# video capture
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#write video in current directory
import os

counter=1
new_name = '13-12/video'
start_time = time.time()
#check if new_name already exists
while os.path.exists(new_name+'.avi'):
    new_name = '13-12/video'+str(counter)
    counter+=1

#check if save file already exists
out = cv2.VideoWriter(new_name+'.avi', fourcc, 20.0, (640, 480))





#start timer




        

start_time = time.time()



# create main function

x2_list = []
counter_list = []
while True:
    
    
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    ret, frame = cap.read()
    if ret == True:
        # write the frame
        out.write(frame)
      
    frame = frame[100:500, 100:500]
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # introduce threshold to make image black and white and make the eye more visible
    _, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    # introduce blur to make the image more clear
    blur = cv2.GaussianBlur(threshold, (5, 5), 0)
    # introduce canny to make the image more clear
    canny = cv2.Canny(blur, 200, 200)
    # introduce dilation to make the image more clear
    kernel = np.ones((5, 5))
   
    rows, cols, _ = frame.shape
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # introduce contours to make the image more clear
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    # introduce contours to make the image more clear
    
  
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        #   introduce contours to make the image more clear
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.line(frame, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        cv2.line(frame, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        
        cv2.circle(frame, (x + int(w / 2), y + int(h / 2)), 2, (0, 0, 255), 2)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)     
        
        cv2.putText(frame, 'x: ' + str(x2) + ' y: ' + str(y2), (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        
        break
    x2 = x + int(w / 2)
    y2 = y + int(h / 2)
    x2_list.append(x2)
    
    string_time = time.strftime("%S", time.gmtime(time.time()-start_time))
    counter_list.append(string_time)
   
        

   
 
   
    
    # Display the resulting frame
    cv2.imshow('gray', frame)
    cv2.imshow('pink', canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        
       
       
        
        break
        
x2_g=np.array(x2_list)
y2_g=np.array(counter_list)
df = pd.DataFrame({'x': x2_g,  'y': y2_g})


#save both x and y coordinates in one csv file
    
count=1
file_name = '13-12/list'
while os.path.exists(file_name+'.csv'):
    file_name = '13-12/list'+str(count)
    count+=1
    
#add df1 and df2 to csv file with two columns

df.to_csv(file_name+'.csv', index=False)


cap.release()
out.release()
cv2.destroyAllWindows()

#check how long one loop takes

# add to github command

# git add .
    
# git commit -m "add new file"

# git push origin master

# git pull origin master



        
