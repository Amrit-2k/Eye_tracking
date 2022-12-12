import cv2
# find cv2 library
# Create a VideoCapture object and read from input file

import pandas as pd
import numpy as np

# video capture
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#write video in current directory
import os

counter=1
current_dir = os.getcwd()


new_name = '13-12/output'



if os.path.exists(new_name + '.avi'):
            new_name = new_name + str(counter)
            counter += 1
    
out = cv2.VideoWriter(new_name+'.avi', fourcc, 20.0, (640, 480))         

# create main function

x2_list = []
counter_list = []
while True:
    # Capture frame-by-frame

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    ret, frame = cap.read()
    if ret == True:
        # write the frame
        out.write(frame)

        # display the resulting frame

    # make frame to show only eye

    # introduce rows and col

    frame = frame[100:300, 100:300]
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # introduce threshold to make image black and white and make the eye more visible
    _, threshold = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)
    # introduce blur to make the image more clear
    blur = cv2.GaussianBlur(threshold, (5, 5), 0)
    # introduce canny to make the image more clear
    canny = cv2.Canny(blur, 100, 200)
    # introduce dilation to make the image more clear
    kernel = np.ones((5, 5))
    #dilation = cv2.dilate(canny, kernel, iterations=1)
    # introduce erosion to make the image more clear
    #erosion = cv2.erode(dilation, kernel, iterations=1)
    # introduce contours to make the image more clear

   
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
        x2_list.append(x2)
        df = pd.DataFrame(x2_list)
        break
    
        
        #add 1 to file name if same file name is used
        

          
        
      
        


    # Display the resulting frame
    cv2.imshow('gray', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        #check if save file already exists
        
        
        break

    # make the code into



cap.release()
out.release()
cv2.destroyAllWindows()

