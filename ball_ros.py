import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import numpy as np
import serial

class CameraSerialNode(Node):
    def __init__(self):
        super().__init__('camera_serial_node')
        self.publisher_ = self.create_publisher(String, 'Serial_in', 10)

        self.device_name = '/dev/ttyACM0'
        self.ser = self.open_serial(self.device_name)
        if not self.ser.is_open:
            self.get_logger().error(f"Serial Fail: could not open {self.device_name}")
            rclpy.shutdown()
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Could not open camera")
            rclpy.shutdown()
        
        self.timer = self.create_timer(0.1, self.timer_callback)

    def open_serial(self, device_name):
        ser = serial.Serial(
            port=device_name,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        return ser

    def timer_callback(self):
        ret, img = self.cap.read()
        if not ret:
            self.get_logger().warn("Captured empty frame")
            return
        
        min_val_blue = 100
        max_val_blue = 172
        min_val_red = 35
        max_val_red = 137
        min_val_yellow = 40
        max_val_yellow = 41

        kernel = np.ones((7, 7), np.uint8)
        size = (640, 480)
        
        # Convert to HSV and mask different colors
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Blue mask
        lower_blue = np.array([107, 101, 91])
        upper_blue = np.array([130, 216, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        res_blue = cv2.bitwise_and(img, img, mask=mask_blue)

        # Yellow mask
        lower_yellow = np.array([0, 64, 89])
        upper_yellow = np.array([60, 255, 255])
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        res_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

        # Red mask
        lower_red1 = np.array([0, 114, 59])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([150, 99, 92])
        upper_red2 = np.array([180, 255, 255])
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        res_red = cv2.bitwise_and(img, img, mask=mask_red)

        # Process each color
        res_blue = self.process_color(res_blue, kernel, min_val_blue, max_val_blue)
        res_yellow = self.process_color(res_yellow, kernel, min_val_yellow, max_val_yellow)
        res_red = self.process_color(res_red, kernel, min_val_red, max_val_red)

        # Detect circles and draw them
        circles_blue = cv2.HoughCircles(res_blue, cv2.HOUGH_GRADIENT, 1, 10, param1=75, param2=25, minRadius=19, maxRadius=55)
        circles_yellow = cv2.HoughCircles(res_yellow, cv2.HOUGH_GRADIENT, 1, 10, param1=75, param2=25, minRadius=19, maxRadius=55)
        circles_red = cv2.HoughCircles(res_red, cv2.HOUGH_GRADIENT, 1, 10, param1=75, param2=25, minRadius=19, maxRadius=55)

        self.draw_circles(img, circles_blue, (255, 0, 0))
        self.draw_circles(img, circles_yellow, (0, 255, 0))
        self.draw_circles(img, circles_red, (0, 0, 255))

        # Send data to Arduino
        self.send_serial_data(circles_blue, 'B')
        self.send_serial_data(circles_yellow, 'Y')
        self.send_serial_data(circles_red, 'R')

        # Display the image
        cv2.imshow('Processed Image', img)
        cv2.waitKey(1)

    def process_color(self, img, kernel, min_val, max_val):
        img = cv2.resize(img, (640, 480))
        img = cv2.GaussianBlur(img, (33, 33), 2)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.Canny(img, min_val, max_val)
        return img

    def draw_circles(self, img, circles, color):
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(img, (i[0], i[1]), i[2], color, 2)
                cv2.circle(img, (i[0], i[1]), 2, color, 3)

    def send_serial_data(self, circles, label):
        if circles is not None:
            data = f"{label}: {len(circles[0])} circles detected"
            self.ser.write(data.encode())
            self.get_logger().info(data)
            msg = String()
            msg.data = data
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CameraSerialNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.cap.release()
    node.ser.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
