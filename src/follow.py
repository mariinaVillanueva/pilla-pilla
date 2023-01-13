#!/usr/bin/env python3
import time
import rospy
from smach import State, StateMachine
import smach_ros
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
#import keyboard
from kobuki_msgs.msg import BumperEvent
from pillapilla.msg import coordenadas


MAX_SPEED = 0.3
ACTUAL_SPEED = 0.0
ESTADO = 0
X = 0
Y = 0
WIDHT = 0
HEIGHT = 0
DETECTED = False
ROBOT = 0
HUMANO = 0

def proporcional_speed(case):
    global ACTUAL_SPEED
    if case == 0:   #acelerar
        ACTUAL_SPEED = ACTUAL_SPEED + 0.01
    elif case == 1: #decelerar
        ACTUAL_SPEED = ACTUAL_SPEED - 0.01

    if ACTUAL_SPEED > MAX_SPEED:
        ACTUAL_SPEED = MAX_SPEED
    if ACTUAL_SPEED < 0:
        ACTUAL_SPEED = 0.0
    
    return ACTUAL_SPEED

def look_forward(scan, length):
    average = 0
    minimum = scan[int((2*length)/5)]
    for i in range(int(2*length/5),int(3*length/5),1):
        average += scan[i]
        if scan[i] < minimum:
            minimum = scan[i]
    average = average/(length/5)
    return (average, minimum)

def look_right(scan, length):
    average = 0
    minimum = scan[0]
    for i in range(0,int(2*length/5),1):
        average += scan[i]
        if scan[i] < minimum:
            minimum = scan[i]
    average = average/(2*length/5)
    return (average, minimum)

def look_left(scan, length):
    average = 0
    minimum = scan[int(3*length/5)]
    for i in range(int(3*length/5),int(length),1):
        average += scan[i]
        if scan[i] < minimum:
            minimum = scan[i]
    average = average/(2*length/5)
    return (average, minimum)

def callback_coordenadas(coord):
    global DETECTED, X, Y, WIDHT, HEIGHT
    if coord.detected:
        DETECTED = True
        X = coord.x
        Y = coord.y
        WIDHT = coord.widht
        HEIGHT = coord.height
    else:
        DETECTED = False
        X = 0
        Y = 0

def callback_movement(scan):
    global ESTADO, ACTUAL_SPEED, ROBOT, X, Y, WIDHT
    speed = Twist()
    tam = int(len(scan.ranges))
    #speed.linear.x = ...
    #speed.angular.z = ...

    # A = average
    # M = medium

    

    (AFront, MFront) = look_forward(scan.ranges, tam)
    
    #EN CASO DEL ROBOT SIMULADO
    #ALeft, MLeft = look_left(scan.ranges, tam)
    #ARight, MRight = look_right(scan.ranges, tam)
    #EN CASO DEL ROBOT REAL
    ALeft, MLeft = look_right(scan.ranges, tam)
    ARight, MRight = look_left(scan.ranges, tam)

    if ESTADO == 0:      #Estado base, espera a poder moverse
        result()
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("Adelante")
        speed.linear.x = proporcional_speed(1)
        speed.angular.z = 0
        if MFront > 0.40:
            ESTADO = 1
        else:
            speed.angular.z = 0.5
    elif ESTADO == 1:    #Estado 1, avanza hasta detectar objeto
        if DETECTED == True:
            ESTADO = 5
        speed.linear.x = proporcional_speed(0)
        if MLeft < 0.50:
            speed.angular.z = -0.4
        elif MRight < 0.50:
            speed.angular.z = 0.4

        if MFront < 0.60:
            ESTADO = 2
    elif ESTADO == 2:    #Estado 2, decide a que lado girar
        speed.linear.x = proporcional_speed(1)
        if ALeft > ARight:
            ESTADO = 4
        elif ARight > ALeft: 
            ESTADO = 3
    elif ESTADO == 3:    #Estado 3, giro al lado derecho
        speed.linear.x = proporcional_speed(1)
        speed.angular.z = -0.7
        if MFront > 0.50:
            ESTADO = 1
    elif ESTADO == 4:    #Estado 4, giro al lado izquierdo
        speed.linear.x = proporcional_speed(1)
        speed.angular.z = 0.7
        if MFront > 0.50:
            ESTADO = 1
    elif ESTADO == 5: #Estado 5, cuando existe detección de objeto 
        if DETECTED == False:
            ESTADO = 1

        speed.linear.x = proporcional_speed(0)
        if X > WIDHT/2:
            vel = ((WIDHT/2)-X)*0.003
            speed.angular.z = vel
        elif X < WIDHT/2:
            vel = ((WIDHT/2)-X)*0.003
            speed.angular.z = vel
        

        # En caso de que se acerque demasiado a las pareces
        if MLeft < 0.50:
            speed.angular.z = -0.6
        elif MRight < 0.50:
            speed.angular.z = 0.6

        if MFront < 0.40:
            ESTADO = 2
        elif MFront < 0.5:
            ROBOT += 1
            speed.linear.x = proporcional_speed(1)
            ESTADO = 0
    #print("Estado ",ESTADO)
    #print(MFront)
    pub.publish(speed)

def callback_bump(data):
    global HUMANO, ESTADO
    HUMANO += 1
    ESTADO = 0

def result():
    global ROBOT, HUMANO
    print("RESULTADO")
    print("Robot    ", ROBOT, "-", HUMANO, "    Humano")


#keyboard.on_press_key("a", result)

rospy.init_node('follow')
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=5)
subs = rospy.Subscriber('/topic_posicion', coordenadas, callback_coordenadas)
sub = rospy.Subscriber('/scan', LaserScan, callback_movement)
subbump = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback_bump)

rospy.spin()












