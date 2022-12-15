import cv2
import pandas as pd
import numpy as np
import time
import os

# video capture
cap = cv2.VideoCapture(0)

# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#check if save file already exists
video_file_counter=1
video_file = '13-12/video'
#check if new_name already exists
while os.path.exists(video_file +'.avi'):
    video_file = '13-12/video'+str(video_file_counter)
    video_file_counter+=1

#save video file
out = cv2.VideoWriter(video_file+'.avi', fourcc, 20.0, (640, 480))
        
#check how long one loop takes
start_time = time.time()

#list for x and time 
x_list = []
time_list = []


while True:  
    # Capture frame-by-frame
    ret, frame = cap.read()  
   
    #check if cap is opened
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
         
    #check if frame is read
    if ret == True:
        # write the frame
        out.write(frame)
     
    #crop frame 
    frame = frame[100:500, 100:500]
    
    # introduce gray to make the image more clear
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # introduce threshold to make image black and white and make the eye more visible
    _, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    
    # introduce blur to make the image more clear
    blur = cv2.GaussianBlur(threshold, (5, 5), 0)
    
    # introduce canny to make the image more clear
    canny = cv2.Canny(blur, 200, 200)
    
    # introduce dilation to make the image more clear
    kernel = np.ones((5, 5))
   
    #find contours of the frame
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # introduce contours to make the image more clear
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
    #rows and cols of the frame
    rows, cols, _ = frame.shape
    for cnt in contours:
        #draw rectangle on the contour
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #drawe lines on the center of the rectangle        
        cv2.line(frame, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        cv2.line(frame, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        
        #draw circle at the center of the darkest part of the eye        
        cv2.circle(frame, (x + int(w / 2), y + int(h / 2)), 2, (0, 0, 255), 2)
        
        #write coordinates of the center of the darkest part of the eye
        font = cv2.FONT_HERSHEY_SIMPLEX
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)             
        cv2.putText(frame, 'x: ' + str(x2) + ' y: ' + str(y2), (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)        
        
        break
    
    #add x2 to list
    x2 = x + int(w / 2)
    x_list.append(x2)
    
    #format time to string and calculate time   
    string_time = time.strftime("%S", time.gmtime(time.time()-start_time))
    #add time to list 
    time_list.append(string_time)
       
    #Display the resulting frame
    cv2.imshow('Frame', frame)
    cv2.imshow('Grey', threshold)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        #save both x and y coordinates in one csv file
        x_dataFrame=np.array(x_list)
        time_dataFranme=np.array(time_list)        
        
        #create dataframe
        df = pd.DataFrame({'x': time_dataFranme,  'y': x_dataFrame})        
        
        #check if save file already exists
        excel_file_counter=1
        excel_file_name = '13-12/list'
        while os.path.exists(excel_file_name+'.csv'):
            excel_file_name = '13-12/list'+str(excel_file_counter)
            excel_file_counter+=1
            
        #add df1 and df2 to csv file with two columns
        df.to_csv(excel_file_name+'.csv', index=False)
                     
        break
        
# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()   

