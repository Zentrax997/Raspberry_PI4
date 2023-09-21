import numpy as np
import cv2
import RPi.GPIO as GPIO
from time import sleep

#Configuracion de pines para motores pw

GPIO.set_mode(GPIO.BCM)
left_motor_forward = 22
left_motor_backward = 23
right_motor_forward = 24
right_motor_backward= 25

#Aca es donde vas a colocar lols pines pw para el motor
left_pwm_pin = 12
right_pwm_pin = 13


#Configuracion de los motores

GPIO.setup(left_motor_forward,GPIO.OUT)
GPIO.setup(left_motor_backward,GPIO.OUT)
GPIO.setup(right_motor_forward,GPIO.OUT)
GPIO.setup(right_motor_backward,GPIO.OUT)

#Configuracion de los pines PWM
GPIO.setup( left_pwm_pin, GPIO.OUT)
GPIO.setup( right_pwm_pin, GPIO.OUT)


left_pwm = GPIO.PWM(left_pwm_pin, 100)
right_pwm = GPIO.PWM(right_pwm_pin, 100)

left_pwm.start(0)
right_pwm.start(0)

#Variables para la velocidad especifica de los motores

left_motor_speed = 25
right_motor_speed = 25

#Funciones para controlar el moviemento

def move_forward():
    GPIO.output(left_motor_forward, GPIO.HIGH)
    GPIO.output(left_motor_backward, GPIO.LOW)
    GPIO.output(left_motor_forward, GPIO.HIGH)
    GPIO.output(left_motor_forward, GPIO.LOW)
    left_pwm.ChangeDutyCycle(left_motor_speed)
    right_pwm.ChangeDutyCycle(right_motor_speed)

def move_backward():
    GPIO.output(left_motor_forward, GPIO.LOW)
    GPIO.output(left_motor_backward, GPIO.HIGH)
    GPIO.output(left_motor_forward, GPIO.LOW)
    GPIO.output(left_motor_forward, GPIO.HIGH)
    left_pwm.ChangeDutyCycle(left_motor_speed)
    right_pwm.ChangeDutyCycle(right_motor_speed)

def right_move():
    GPIO.output(left_motor_forward, GPIO.HIGH)
    GPIO.output(right_motor_forward,GPIO.LOW)
    left_pwm.ChangeDutyCycle(left_motor_speed)
    right_pwm.ChangeDutyCycle(right_motor_speed)

def left_move():
    GPIO.output(left_motor_forward, GPIO.LOW)
    GPIO.output(right_motor_forward,GPIO.HIGH)
    left_pwm.ChangeDutyCycle(left_motor_speed)
    right_pwm.ChangeDutyCycle(right_motor_speed)

def stop():
    GPIO.output(left_motor_forward, GPIO.LOW)
    GPIO.output(left_motor_backward, GPIO.LOW)
    GPIO.output(left_motor_forward, GPIO.LOW)
    GPIO.output(left_motor_forward, GPIO.LOW)




#Recuerde tener en la raspberry PI 4 , conectada el flex que se llama camara


#Configuracion para la camara


video_capture = cv2.VideoCapture(-1)
video_capture.set(3,160)
video_capture.set(4,120)

while(True):
    
    ret, frame = video_capture.read()

    crop_img = frame [60:120, 0:160]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5)0)
    ret, thresh1 = cv2.threshold(blur,25,255,cv2.THRESH_BINARY_INV)

    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask,None, iterations=2)

    contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        C = max(contours, key=cv2.contourArea)
        M = cv2.moments(C)

    cx= int(M["m10"] / M ["m00"] )
    cy = int(M["m01"] / M ["m00"] )

    cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
    cv2.line(crop_img,(0,cy)(1280,cy),(255,0,0),1)


    cv2.drawContours(crop_img,contours,-1 (0,255,0),1)
    print(cx)
    print(cy)

    if cx >= 120:
        left_motor_speed
        right_motor_speed
        right_move()
    if cx < 120 and cx > 50:
        move_forward()
        left_motor_speed
        right_motor_speed
    if cx <= 50:
        left_move()
        left_motor_speed
        right_motor_speed
    else:
        stop()
    cv2.imshow("Capturando Video", crop_img)
    if cv2.waitKey(1) & 0xFF == ord ("Q"): #Presiona Q para cerrar la pestaña
        break


    














