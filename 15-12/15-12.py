import cv2
import pandas as pd
import numpy as np
import time
import os

FPS= 20.0
FRAME_SIZE = (640, 480)

OUTPUT_VIDEO_NAME = 'output'
OUTPUT_VIDEO_EXTENSION = '.avi'

OUTPUT_FILE_NAME = 'excel'
OUTPUT_FILE_EXTENSION = '.csv'


def get_file_name(file_name, file_extension):    

   return file_name + file_extension


# video capture
def initialise_cam():
    try:
        cap = cv2.VideoCapture(0)

    except:
        print("Error opening video stream or file")
    
    return cap

def initialise_video_writer(file_path):
      
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  
    #check if save file already exists
    out = cv2.VideoWriter( file_path, fourcc, FPS, (FRAME_SIZE))
    return out

def check_if_file_exists(file_path):
    if os.path.exists(file_path):
        return True
    return False

def create_new_file_name(file_name, file_extension, file_count):
    
    file_name = file_name + str(file_count)
    
    file_path = get_file_name(file_name, file_extension)

    if check_if_file_exists(file_path):
        
        file_count += 1
        create_new_file_name(file_name, file_extension, file_count) 

    return file_path


def edit_frame(frame):
    x2=0

    frame = frame[100:500, 100:500]
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # introduce threshold to make image black and white and make the eye more visible
    _, threshold = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY_INV)
    # introduce blur to make the image more clear
    blur = cv2.GaussianBlur(threshold, (7, 7), 0)    
    #make image more stable
    canny = cv2.Canny(blur, 50, 150)      
 
    rows, cols, _ = frame.shape
    contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # introduce contours to make the image more clear
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=  False)
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

    return frame, x2



def run(count):
    
    time_list = []
    x2_list = []
    start_time = time.time()
    cap = initialise_cam()
    file_path = create_new_file_name(OUTPUT_VIDEO_NAME, OUTPUT_VIDEO_EXTENSION, count)    
    out = initialise_video_writer(file_path)    

    while True:
        ret, frame = cap.read()
        if ret == True:
            # write the frame
            frame, x2 = edit_frame(frame)    
            out.write(frame) 
        else:
            break

        string_time = time.strftime("%S", time.gmtime(time.time()-start_time))
        
        time_list.append(string_time)
        x2_list.append(x2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            exit()
            
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return time_list, x2_list

def save_to_csv(time_list, x2_list, file_count):
    
        
    x_values=np.array(x2_list)
    time_values=np.array(time_list)
    df = pd.DataFrame({'time': time_values,  'x Value': x_values})

    #check if file already exists
    file_path = create_new_file_name(OUTPUT_FILE_NAME, OUTPUT_FILE_EXTENSION, file_count)
    
    #add df1 and df2 to csv file with two columns
    df.to_csv(file_path, index=False)





def main():
    count = 1

    while True:
             
        time_list, x2_list = run(count)
        save_to_csv(time_list, x2_list, count)
        count += 1

if __name__ == '__main__':
    main()
    