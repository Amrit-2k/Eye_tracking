# Author: Addison Sears-Collins
# Description: This algorithm detects objects in a video stream
#   using the Absolute Difference Method. The idea behind this 
#   algorithm is that we first take a snapshot of the background.
#   We then identify changes by taking the absolute difference 
#   between the current video frame and that original 
#   snapshot of the background (i.e. first frame). 
 
# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np # Import NumPy library
import pandas as pd

camera = PiCamera()
# Set the camera resolution
camera.resolution = (320, 240)
 
# Set the number of frames per second
camera.framerate = 60
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(320, 240))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(1)
 
# Initialize the first frame of the video stream
first_frame = None
 
# Create kernel for morphological operation. You can tweak
# the dimensions of the kernel.
# e.g. instead of 20, 20, you can try 30, 30
kernel = np.ones((20,20),np.uint8)


# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
   
    # Grab the raw NumPy array representing the image
    image = frame.array
    
    
    rows, cols, _ = image.shape
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     
    # Close gaps using closing
    gray = cv2.GaussianBlur(gray,(7,7),0)
    
    # Remove salt and pepper noise with a median filter
    _, threshold = cv2.threshold(gray,10, 255, cv2.THRESH_BINARY_INV)
     
    # If first frame, we need to initialize it.
    if first_frame is None:
        
      first_frame = gray       
      # Clear the stream in preparation for the next frame
      raw_capture.truncate(0)       
      # Go to top of for loop
      continue
    else:
        #
        contours, _ = cv2.findContours (threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)        
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            x2=0
            x2 = x + int(w/2)
            y2 = y + int(h/2)
            cv2.circle(image,(x2,y2),4,(0,0,255),2)
            cv2.line(image, (x+int(w/2),0), (x+int(w/2),rows), (0, 255, 0),2)
            cv2.line(image, (0,y+int(h/2)), (cols, y+int(h/2)), (0,255, 0),2)
            
            text = "x: " + str(x2) + ", y: " + str(y2)
            cv2.putText(image, text, (x2 - 10, y2 - 10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
           
    
            xValue = [x2]
            for x2 in xValue:
                print(xValue)
            
            """     
        
          
            data = pd.DataFrame({"x":xValue})
            for x2 in data:
               data.to_excel('sample.xlsx', sheet_name='sheet1', index=False)
            break
            
             with open(r'sample.txt', 'w') as fp:
                    for line in fp:
                        x = line[:-1]
                        xValue.append(x)"""
                            
            
        
        #cv2.drawContours(image, cnt, -1, (255,0,0), 3)
   
    cv2.imshow("gray", image)   
    key = cv2.waitKey(1) & 0xFF
   
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
   
    # If "q" is pressed on the keyboard, 
    # exit this loop
    if key == ord("q"):
         
       break

"""
     with pd.ExcelWriter ("sample.xlsx", mode="a", engine = "openpyxl") as writer:
        data.to_excel(writer, sheet_name = "sheet3")
  """
# Close down windows
cv2.destroyAllWindows()