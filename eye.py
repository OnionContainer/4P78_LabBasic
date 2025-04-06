import cv2
import numpy as np


#video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
video = cv2.VideoCapture("IMG_9828.MOV")

lower_b = np.array([20, 20, 20]) #In future: add option to switch range based on eye color
upper_b = np.array([180, 255, 70])

#(93, 48, 59)

# For testing window x,y location using mouse 
# def show_xy(event, x, y, flags, param):# Detect mouse movement for testing
#     if event == cv2.EVENT_MOUSEMOVE:  
#         print(f"Mouse Position - x: {x}, y: {y}")

# Set the mouse callback to display coordinates+


while True:
    success, frame = video.read()


    ####################maybe move some of these out of the while loop later######################

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) #Video was sideways
    cropped = frame[600:900, 300:700] #Crop to eye

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert to hsv
    mask = cv2.inRange(hsv,lower_b,upper_b) #new window (bit-mask) showing only colors in range
    
    mask_crop = mask[600:900, 300:700]


    contours_black, h = cv2.findContours(mask_crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    

    cv2.imshow("Mask",mask_crop) 
    

    
    height, width = cropped.shape[:2] #size of frame

    w2 = width // 2 
    h2 = height // 2 

    #grey_scale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY) #Greyscale

    #x,y axis 
    cv2.line(img=cropped, pt1=(0, h2), pt2=(width, h2), color=(8, 108, 255), thickness=3, lineType=8, shift=0)
    cv2.line(cropped, (w2, 0), (w2, height), (8, 108, 255), 3, 8, 0)


    #loop through each contour (white area) in the bit-mask
    for contour in contours_black:
        if cv2.contourArea(contour) > 3000 and cv2.contourArea(contour) < 25000: #May need to be adjusted later 
            x, y, w, h = cv2.boundingRect(contour) #rectangle over the eye

            #getting center mass
            eye_x =  x + w//2
            eye_y = y + h//2

            cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)  
            cv2.putText(cropped, "Eye", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (169, 169, 169), 2)
            cv2.putText(cropped, f"x: {x} y: {y}", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (169, 169, 169), 2)
            cv2.putText(cropped, f"mx: {eye_x} my: {eye_y}", (x, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (169, 169, 169), 2)

            cv2.circle(cropped,(eye_x, eye_y), 30, (0,255,0))  #center of mass (pupil)
            
            #print(middle_x,middle_y)
            

            # 0 = open
            # 1 = half open
            # 2 = closed

            eye = 0 
            #Based on area of iris
            if cv2.contourArea(contour) > 9000: 
                #print ("O O") #Open 
                eye = 0
            elif cv2.contourArea(contour) <= 9000:
                #print(". .") #Half Open
                eye = 1  
            elif cv2.contourArea(contour) < 6000:
                #print("_ _") #Close 
                eye = 2

                


                
    # cv2.namedWindow("Ola")
    # cv2.setMouseCallback("Ola", show_xy)

    cv2.imshow("Ola", cropped)


    if cv2.waitKey(100) & 0xFF == ord('q'):  #wait 100 is to slow down video for analyzing 
        break


video.release()
cv2.destroyAllWindows()
