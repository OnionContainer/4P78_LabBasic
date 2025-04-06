import cv2
import numpy as np

class EyeDetection:

    def __init__(self, video_path):


        self.video = cv2.VideoCapture(video_path)
        self.lower_b = np.array([20, 20, 20])  #In future: add option to switch range based on eye color
        self.upper_b = np.array([180, 255, 70])

    def process_frame(self): #process one frame
        success, frame = self.video.read()

        if not success:
            return False  # Return False if no more frames are available

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  #Video was sideways
        cropped = frame[600:900, 300:700]  #Crop to eye

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #Convert to HSV color space
        mask = cv2.inRange(hsv, self.lower_b, self.upper_b)  #Create mask for color range

        mask_crop = mask[600:900, 300:700]  #Crop mask to eye

        contours_black, _ = cv2.findContours(mask_crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width = cropped.shape[:2]  #Size of frame
        w2 = width // 2
        h2 = height // 2

        #Draw center lines on the cropped frame
        cv2.line(cropped, (0, h2), (width, h2), (8, 108, 255), 3, 8, 0)
        cv2.line(cropped, (w2, 0), (w2, height), (8, 108, 255), 3, 8, 0)

        #Loop through each contour (white area) in the bitmask
        for contour in contours_black:
            if cv2.contourArea(contour) > 3000 and cv2.contourArea(contour) < 25000:  
                x, y, w, h = cv2.boundingRect(contour)  #rectangle around eye

                #Getting center mass of the eye
                eye_x = x + w // 2
                eye_y = y + h // 2

                cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle
                cv2.putText(cropped, "Eye", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (169, 169, 169), 2)
                cv2.putText(cropped, f"x: {x} y: {y}", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (169, 169, 169), 2)
                cv2.putText(cropped, f"mx: {eye_x} my: {eye_y}", (x, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (169, 169, 169), 2)

                cv2.circle(cropped, (eye_x, eye_y), 30, (0, 255, 0))  # Draw circle at center mass (pupil)

            #0 = open
            #1 = half open
            #2 = closed

            eye_state = 0  
            if cv2.contourArea(contour) > 9000:
                eye_state = 0  # Open
            elif 6000 < cv2.contourArea(contour) <= 9000:
                eye_state = 1  # Half open
            elif cv2.contourArea(contour) <= 6000:
                eye_state = 2  # Closed

        #cv2.imshow("Eye Detection", cropped)

        #emit

        return True  #Return True if there was a frame

if __name__ == "__main__":
    
    eye_detection = EyeDetection("IMG_9828.MOV")
    if not eye_detection.process_frame():
        print("NO FRAMES ):")


    """
    while True:
        if not eye_detection.process_frame():  #Process each frame
            break  #If no more frames are available  break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  #Wait for 'q' to quit
            break
    """

    #eye_detection.video.release()
    #cv2.destroyAllWindows()
