import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import serial
import time

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
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Captured empty frame")
            return
        
        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()
        
        try:
            self.ser.write(data)
            self.get_logger().info(f"Sent {len(data)} bytes")
            
            msg = String()
            msg.data = f"Sent {len(data)} bytes"
            self.publisher_.publish(msg)
        except serial.SerialTimeoutException:
            self.get_logger().error("Failed to write to serial port")

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