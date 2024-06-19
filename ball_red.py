import cv2
import numpy as np


def nothing(x):
    pass
cv2.namedWindow('trackbar')
cv2.namedWindow('Edges')

cv2.namedWindow('Edge')
cv2.createTrackbar("threshold1","Edge", 43, 200, nothing)
cv2.createTrackbar("threshold2","Edge", 41, 200, nothing)
cv2.createTrackbar("mindist", "Edges", 10, 100, nothing)
cv2.createTrackbar("pra1", "Edges", 75, 100, nothing)
cv2.createTrackbar("pra2", "Edges", 30, 100, nothing)
cv2.createTrackbar("minRad", "Edges", 10, 100, nothing)
cv2.createTrackbar("maxRad", "Edges", 60, 100, nothing)


cv2.createTrackbar("H_l", "trackbar", 0, 180, nothing)
cv2.createTrackbar("H_h", "trackbar", 10, 180, nothing)
cv2.createTrackbar("S_l", "trackbar", 114, 255, nothing)
cv2.createTrackbar("S_h", "trackbar", 255, 255, nothing)
cv2.createTrackbar("V_l", "trackbar", 59, 255, nothing)
cv2.createTrackbar("V_h", "trackbar", 255, 255, nothing)
cv2.createTrackbar("H_l1", "trackbar", 150, 180, nothing)
cv2.createTrackbar("H_h1", "trackbar", 180, 180, nothing)
cv2.createTrackbar("S_l1", "trackbar", 99, 255, nothing)
cv2.createTrackbar("S_h1", "trackbar", 255, 255, nothing)
cv2.createTrackbar("V_l1", "trackbar", 92, 255, nothing)
cv2.createTrackbar("V_h1", "trackbar", 255, 255, nothing)




def pick_up_ball():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    min_val_blue = 98
    max_val_blue = 257

    min_val_red = 35
    max_val_red = 137

    
    

    


    kernel = np.ones((3,3),np.uint8)
    kernel1 = np.ones((5, 5), np.uint8)

    while True:
        ret,img = cap.read()
        size = (640,480)
        cimg1 = img

        h_l = cv2.getTrackbarPos("H_l", "trackbar")
        h_h = cv2.getTrackbarPos("H_h", "trackbar")
        s_l = cv2.getTrackbarPos("S_l", "trackbar")
        s_h = cv2.getTrackbarPos("S_h", "trackbar")
        v_l = cv2.getTrackbarPos("V_l", "trackbar")
        v_h = cv2.getTrackbarPos("V_h", "trackbar")

        h_l1 = cv2.getTrackbarPos("H_l1", "trackbar")
        h_h1= cv2.getTrackbarPos("H_h1", "trackbar")
        s_l1= cv2.getTrackbarPos("S_l1", "trackbar")
        s_h1 = cv2.getTrackbarPos("S_h1", "trackbar")
        v_l1= cv2.getTrackbarPos("V_l1", "trackbar")
        v_h1 = cv2.getTrackbarPos("V_h1", "trackbar")

        # Convert to hsv
        # blue
        hsv_blue = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([h_l, s_l, v_l])
        upper_blue = np.array([h_h, s_h, v_h])
        img_mask_blue = cv2.inRange(hsv_blue, lower_blue, upper_blue)
        img_color_blue = cv2.bitwise_and(img, img, mask=img_mask_blue)

        #yellow
        hsv_yellow = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([h_l, s_l, v_l])
        upper_yellow = np.array([h_h, s_h, s_h])
        img_mask_yellow = cv2.inRange(hsv_yellow, lower_yellow, upper_yellow)
        img_color_yellow = cv2.bitwise_and(img, img, mask=img_mask_yellow)

        #red
        hsv_red = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([h_l, s_l, v_l])
        upper_red1 = np.array([h_h, s_h, v_h])    
        lower_red2 = np.array([h_l1, s_l1, v_l1])
        upper_red2 = np.array([h_h1, s_h1, v_h1])
        img_mask_red1 = cv2.inRange(hsv_red, lower_red1, upper_red1)
        img_mask_red2 = cv2.inRange(hsv_red, lower_red2, upper_red2)
        img_mask_red = cv2.bitwise_or(img_mask_red1, img_mask_red2)
        img_color_red= cv2.bitwise_and(img, img, mask=img_mask_red)


        threshold1 = cv2.getTrackbarPos("threshold1","Edge")
        threshold2 = cv2.getTrackbarPos("threshold2","Edge")
        mindist = cv2.getTrackbarPos("mindist", "Edges")
        pra1 = cv2.getTrackbarPos("pra1", "Edges")
        pra2 = cv2.getTrackbarPos("pra2", "Edges")
        minRad = cv2.getTrackbarPos("minRad", "Edges")
        maxRad = cv2.getTrackbarPos("maxRad", "Edges")


        #a = cv2.getTrackbarPos("futosa", "a")

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
        
       

        #cimg2 = img_color_blue

        #cimg4 = img_color_red
        cimg2 = img_color_red


        img_color_blue = cv2.cvtColor(img_color_blue, cv2.COLOR_RGB2GRAY)
        img_color_yellow = cv2.cvtColor(img_color_yellow, cv2.COLOR_RGB2GRAY)
        img_color_red = cv2.cvtColor(img_color_red, cv2.COLOR_RGB2GRAY)

        cimg4 = img_color_yellow

        #opening closing

        img_color_red = cv2.Canny(img_color_red, min_val_red, max_val_red)
        img_color_yellow = cv2.Canny(img_color_yellow, threshold1, threshold2)
        
        img_color_blue = cv2.Canny(img_color_blue, min_val_blue, max_val_blue) #o
        
        cimg3 = img_color_red

        







        #circles1 = cv2.HoughCircles(img_color_blue,cv2.HOUGH_GRADIENT,1,10,param1= 80, param2=18,minRadius= 10,maxRadius=30) #ok
        circles3 = cv2.HoughCircles(img_color_red, cv2.HOUGH_GRADIENT, 1, mindist, param1=pra1, param2=pra2, minRadius=minRad, maxRadius=maxRad)
        #circles3 = cv2.HoughCircles(img_color_red,cv2.HOUGH_GRADIENT,1,10,param1=80,param2=18,minRadius= 10,maxRadius=30)

        if circles3 is not None:
            circles3 = np.uint16(np.around(circles3))
            for j in circles3[0, :]:
                cv2.circle(cimg1, (j[0], j[1]), j[2], (0, 255, 0), 2)
                cv2.circle(cimg1, (j[0], j[1]), 2, (0, 0, 255), 3)


        else:
            print("nothing")

        cv2.imshow('orizin',cimg1)
        cv2.imshow('redmask',cimg2)
        cv2.imshow('red', cimg3)
        #cv2.imshow('red', cimg4)


        k = cv2.waitKey(10)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pick_up_ball()