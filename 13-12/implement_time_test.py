
import cv2 # OpenCV library
import numpy as np # Import NumPy library
import pandas as pd
#create a class 

class EyeTracking:
    def __init__(self):
       
        self.cap = cv2.VideoCapture(0)
        self.x2_list = []
        self.counter_list = []
        self.counter = 0
        self.x2 = 0
        self.y2 = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, (640, 480))
        self.kernel = np.ones((20,20),np.uint8)

    def run(self):
        while True:
# Capture frame-by-frame
            ret, frame = self.cap.read()      
            if (self.cap.isOpened() == False) & (ret == False):
                print("Error opening video stream or file")
                
              
            self.out.write(frame)                        
            self.frame = frame[100:300, 100:300]
            # Our operations on the frame come here
            self.rows,self.cols, _ = self.frame.shape
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # introduce threshold to make image black and white and make the eye more visible
            
            _, threshold = cv2.threshold(gray, 12, 255, cv2.THRESH_BINARY)
            # introduce blur to make the image more clear
            
            blur = cv2.GaussianBlur(threshold, (5, 5), 0)
            # introduce canny to make the image more clear
            
            canny = cv2.Canny(blur, 100, 200)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                self.out.release()
                cv2.destroyAllWindows()
                break
            
#create a function for contours
    def get_contours(frame):
        _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        return contours
    
    #create a function to draw contours
    def draw_contours(self,frame, contours):
        for cnt in contours:        
            (x, y, w, h) = cv2.boundingRect(cnt)
            #   introduce contours to make the image more clear
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.line(frame, (x + int(w / 2), 0), (x + int(w / 2), self.rows), (0, 255, 0), 2)
            cv2.line(frame, (0, y + int(h / 2)), (self.cols, y + int(h / 2)), (0, 255, 0), 2)
            cv2.circle(frame, (x + int(w / 2), y + int(h / 2)), 2, (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            x2 = x + int(w / 2)
            y2 = y + int(h / 2)
            self.x2_list.append(x2)
            cv2.putText(frame, 'x: ' + str(x2) + ' y: ' + str(y2), (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
    
    #def save to excel
    def save_to_excel(self):
        df = pd.DataFrame(self.x2_list)
        df.to_csv('x2_list.csv',mode='a', index=False)

   

#run the program
if __name__ == '__main__':
    eye_tracking = EyeTracking()
    eye_tracking.run()
    eye_tracking.get_contours()
    eye_tracking.draw_contours()
    eye_tracking.save_to_excel()
    