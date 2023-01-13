#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import CompressedImage
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from pillapilla.msg import coordenadas

def callback(data):
    msg = coordenadas()

    #bridge = CvBridge()

    # Pasar la imagen de ROS a openCV
    #cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')

    # Si la imagen está en espejo
    # cv_image = cv2.flip(cv_image, 1)

    # Pasar la imagen de ROS a openCV
    np_arr = np.frombuffer(data.data, np.uint8)
    cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    # Se filtra el color azul
    mask = cv2.inRange(hsv, (100, 100, 20),(125, 255, 255))
    # Se detecta el contorno de las zonas azules
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        c = max(contornos, key=cv2.contourArea) 
        area = cv2.contourArea(c)
        if area > 500:
            M = cv2.moments(c)
            msg.detected = True
            if (M["m00"]==0):
                M["m00"]=1
            msg.x = int(M["m10"]/M["m00"])
            msg.y = int(M["m01"]/M["m00"])
            msg.widht, msg.height, _ = cv_image.shape
            # Marca en la imagen el centro de la zona detectada en color azul
            cv2.circle(cv_image, (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])), 7, (0,0,255), -1)
        else:
            msg.x, msg.y, msg.widht, msg.height = 0,0,0,0
            msg.detected = False

    pub = rospy.Publisher('/topic_posicion', coordenadas, queue_size=10)
    pub.publish(msg)


def recepcion():
    rospy.init_node('lecturaCamara', anonymous=True)
    rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, callback)
    rospy.spin()


if __name__ == '__main__':
    recepcion()









