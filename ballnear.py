import cv2
import numpy as np


def nothing(x):
    pass
cv2.namedWindow('trackbar')



def pick_up_ball():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    min_val_blue = 100
    max_val_blue = 172

    min_val_red = 35
    max_val_red = 137

    min_val_yellow = 40
    max_val_yellow = 41

    

    


    kernel = np.ones((7,7),np.uint8)

    while True:
        ret,img = cap.read()
        size = (640,480)
        cimg1 = img

        # Convert to hsv
        # blue
        hsv_blue = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([107, 101, 91])
        upper_blue = np.array([130, 216, 255])
        img_mask_blue = cv2.inRange(hsv_blue, lower_blue, upper_blue)
        img_color_blue = cv2.bitwise_and(img, img, mask=img_mask_blue)

        #yellow
        hsv_yellow = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([0, 64, 89])
        upper_yellow = np.array([60, 255, 255])
        img_mask_yellow = cv2.inRange(hsv_yellow, lower_yellow, upper_yellow)
        img_color_yellow = cv2.bitwise_and(img, img, mask=img_mask_yellow)

        #red
        hsv_red = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 114, 59])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([150, 99, 92])
        upper_red2 = np.array([180, 255, 255])
        img_mask_red1 = cv2.inRange(hsv_red, lower_red1, upper_red1)
        img_mask_red2 = cv2.inRange(hsv_red, lower_red2, upper_red2)
        img_mask_red = cv2.bitwise_or(img_mask_red1, img_mask_red2)
        img_color_red= cv2.bitwise_and(img, img, mask=img_mask_red)




        # Hough_tranceration
        #blue
        img = img[:,::-1]
        img_color_blue = cv2.resize(img_color_blue, size)
        img_color_blue = cv2.GaussianBlur(img_color_blue, (33,33), 2)
        #yellow
        img_color_yellow = cv2.resize(img_color_yellow, size)
        img_color_yellow = cv2.GaussianBlur(img_color_yellow, (33,33), 2)
        #red
        img_color_red = cv2.resize(img_color_red, size)
        img_color_red= cv2.GaussianBlur(img_color_red, (33,33), 2)
        
       

        cimg2 = img_color_blue
        cimg4 = img_color_red


        img_color_blue = cv2.cvtColor(img_color_blue, cv2.COLOR_RGB2GRAY)
        img_color_yellow = cv2.cvtColor(img_color_yellow, cv2.COLOR_RGB2GRAY)
        img_color_red = cv2.cvtColor(img_color_red, cv2.COLOR_RGB2GRAY)

        #opening closing
        img_color_yellow = cv2.morphologyEx(img_color_yellow, cv2.MORPH_OPEN, kernel)
        img_color_yellow = cv2.morphologyEx(img_color_yellow, cv2.MORPH_CLOSE, kernel)
        img_color_blue = cv2.morphologyEx(img_color_blue, cv2.MORPH_OPEN, kernel)
        img_color_blue = cv2.morphologyEx(img_color_blue, cv2.MORPH_CLOSE, kernel)
        img_color_red = cv2.morphologyEx(img_color_red, cv2.MORPH_OPEN, kernel)
        img_color_red = cv2.morphologyEx(img_color_red, cv2.MORPH_CLOSE, kernel)


        img_color_red = cv2.Canny(img_color_red, min_val_red, max_val_red)
        img_color_yellow = cv2.Canny(img_color_yellow, min_val_yellow, max_val_yellow)
        cimg3 = img_color_yellow

        img_color_blue = cv2.Canny(img_color_blue, min_val_blue, max_val_blue) #ok

        






        circles1 = cv2.HoughCircles(img_color_blue,cv2.HOUGH_GRADIENT,1,10,param1= 75, param2=25,minRadius=19,maxRadius=55) #ok
        circles2 = cv2.HoughCircles(img_color_yellow,cv2.HOUGH_GRADIENT,1,10,param1=75,param2=25,minRadius=19,maxRadius=55)
        circles3 = cv2.HoughCircles(img_color_red,cv2.HOUGH_GRADIENT,1,10,param1=75,param2=25,minRadius=19,maxRadius=55)
        if circles1 is not None:
            circles1 = np.uint16(np.around(circles1))
            for i in circles1[0, :]:
                cv2.circle(cimg1, (i[0], i[1]), i[2], (255, 0, 0), 2)
                cv2.circle(cimg1, (i[0], i[1]), 2, (0, 0, 255), 3)

        if circles2 is not None:
            circles2 = np.uint16(np.around(circles2))
            for j in circles2[0, :]:
                cv2.circle(cimg1, (j[0], j[1]), j[2], (0, 255, 0), 2)
                cv2.circle(cimg1, (j[0], j[1]), 2, (0, 0, 255), 3)

        if circles3 is not None:
            circles3 = np.uint16(np.around(circles3))
            for k in circles3[0, :]:
                cv2.circle(cimg1, (k[0], k[1]), k[2], (255, 255, 0), 2)
                cv2.circle(cimg3, (k[0], k[1]), 2, (0, 0, 255), 3)

        else:
            print("nothing")

        cv2.imshow('orizin',cimg1)
        cv2.imshow('blue',cimg2)
        cv2.imshow('yellow', cimg3)
        cv2.imshow('red', cimg4)


        k = cv2.waitKey(10)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pick_up_ball()