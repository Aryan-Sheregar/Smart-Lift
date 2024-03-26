import cv2
import time
from gpiozero import LED
from signal import pause

#Using pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

red_led = LED(17)
green_led = LED(27)
blue_led = LED(22)

red_led.on()
green_led.off()
blue_led.off()

cap = cv2.VideoCapture(0)

start_time = None
while True:
    ret, img = cap.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) > 0:
  
        red_led.off()
        green_led.on()
        blue_led.off()
        start_time = time.time()  
    elif start_time is not None and time.time() - start_time > 10:
        
        red_led.on()
        green_led.off()
        blue_led.off()
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Frame', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
