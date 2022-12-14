import cv2
import pandas as pd
import numpy as np
import time
import os
#import video.py file
import videoFile
from videoFile import VideoFormat
#import eye.py file

import excel_file

from excel_file import ExcelFile

#inherit video format and excel file class


class EyeTracking(VideoFormat,ExcelFile):
    #create constructor
    def __init__(self): 
        self.video = cv2.VideoCapture(video_file)
        
    #function that check if same video file is saved
     
        #check if save file already exists
        video_file_counter=1
        video_file = 'video'
        
        #check if new_name already exists
        while os.path.exists(video_file +'.avi'):
            video_file = 'video'+str(video_file_counter)
            video_file_counter+=1
        
    
    #define video writer object
   
        #define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #save video file
        out = cv2.VideoWriter(self.check_if_video_file_exists()+'.avi', fourcc, 20.0, (640, 480))
        
        
        #create start time
        self.start_time = time.time()
        
        #create x and time list
        self.x_list = []
        self.time_list = []

       
#define main function
    def main(self):         

        while True:  
            # Capture frame-by-frame    
            ret, self.frame = self.video.read()
            
            #check if cap is opened
            if (self.video.isOpened() == False):
                print("Error opening video stream or file")
                
            #check if frame is read
            if ret == False:
                print("gg")
                break
            # write the frame
            self.video.write(self.frame)   
            self.frame = self.frame[100:500, 100:500] 
            #crop frame 
            
             
           
            
            #run find eye function
            self.find_eye()
            
            #run find contours
            self.create_contours()                        
            #show frame
            cv2.imshow('frame', self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):        
                
                        
                            
                break
                
    #create function that finds the eye
    def find_eye(self):
        # introduce gray to make the image more clear
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        #use threshold to make image black and white and make the eye more visible
        _, self.threshold = cv2.threshold(self.gray, 25, 255, cv2.THRESH_BINARY)

        # introduce blur to make the image more clear
        self.blur = cv2.GaussianBlur(self.threshold, (5, 5), 0)
        
        # introduce canny to make the image more clear
        self.canny = cv2.Canny(self.blur, 200, 200)

        # introduce dilation to make the image more clear
        self.kernel = np.ones((5, 5))
        
    #create function that create contours and the lines
    def create_contours(self):
        #   #find contours of the frame
        contours, _ = cv2.findContours(self.canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # introduce contours to make the image more clear
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        
        #find contours of the frame
        contours, _ = cv2.findContours(self.canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # introduce contours to make the image more clear
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        
        #rows and cols of the frame
        rows, cols, _ = self.frame.shape
        for cnt in contours:
            #draw rectangle on the contour
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            #drawe lines on the center of the rectangle        
            cv2.line(self.frame, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(self.frame, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
            
            #draw circle at the center of the darkest part of the eye        
            cv2.circle(self.frame, (x + int(w / 2), y + int(h / 2)), 2, (0, 0, 255), 2)
            
            #write coordinates of the center of the darkest part of the eye
            font = cv2.FONT_HERSHEY_SIMPLEX
            self.x2 = x + int(w / 2)
            self.y2 = y + int(h / 2)             
            cv2.putText(self.frame, 'x: ' + str(self.x2) + ' y: ' + str(self.y2), (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)        
            
            break
        self.x2 = x + int(w / 2)
        self.x_list.append(self.x2)            
        #format time to string and calculate time   
        string_time = time.strftime("%S", time.gmtime(time.time()-self.start_time))
        #add time to list 
        self.time_list.append(string_time)

#realease video capture object
    def release_video(self):
        self.video.release()
        self.out.release()
       
# Closes all the frames
cv2.destroyAllWindows()   
#run class
if __name__ == "__main__":
    #create object
    eye = EyeTracking()
    #run main function
    eye.main()
    #run release video function
    eye.release_video()
    #run create excel function
    eye.create_excel_file()


        

