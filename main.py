import cv2
import time
from gpiozero import LED, Button
from picamera2 import Picamera2
import numpy as np

camera = Picamera2()
camera.configure(camera.create_preview_configuration())
camera.start()

time.sleep(2)

# Using pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    '/home/pi/haarcascade_frontalface_default.xml')

# Initialize the white LED on GPIO pin 17
white_led = LED(17)

# Initialize the button on GPIO pin 27
button = Button(27)

white_led.off()

# Variables to keep track of button and face detection
button_press_start_time = None
button_pressed = False
face_detected_start_time = None


def but_pres():
    global button_press_start_time, button_pressed
    print("Button pressed")
    button_pressed = True
    button_press_start_time = time.time()
    # Turn on the LED when button is pressed
    white_led.on()


def but_released():
    global button_pressed
    button_pressed = False


button.when_pressed = but_pres
button.when_released = but_released

while True:
    # Capture a frame from the camera
    frame = camera.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if any faces are detected
    face_detected = len(faces) > 0

    if face_detected:
        # Face detected
        white_led.on()
        face_detected_start_time = time.time()  # Reset the face detected timer
    else:
        # No face detected
        if face_detected_start_time is not None and time.time() - face_detected_start_time > 10:
            # No faces detected for more than 10 seconds
            white_led.off()

    # Check if the button was pressed and handle the LED logic
    if button_pressed:
        if time.time() - button_press_start_time < 10:
            # Keep the LED on for 10 seconds when the button is pressed
            white_led.on()
        else:
            # Button pressed for more than 10 seconds, LED will follow face detection logic
            button_pressed = False  # Reset button pressed state
            button_press_start_time = None
            # If no face is detected, turn off the LED
            if not face_detected:
                white_led.off()

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.close()
cv2.destroyAllWindows()
