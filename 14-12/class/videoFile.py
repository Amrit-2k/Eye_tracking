#create video format class
import cv2
import os

class VideoFormat:
    #create video capture object
    def __init__(self, video_file):
        #create video capture object
        
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
        
    

        