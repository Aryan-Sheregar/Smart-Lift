import cv2
import time
from gpiozero import LED, Button
from picamera2 import Picamera2

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration())
camera.start()

time.sleep(2)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')

# Initialize GPIO components
white_led = LED(17)
button = Button(27)

# Initialize flags and timers
button_flag = False
last_face_detected_time = None

def but_pres():
    global button_flag
    print("Button pressed")
    button_flag = True

button.when_pressed = but_pres

try:
    while True:
        # Capture a frame from the camera
        frame = camera.capture_array()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Update face detection time
        if len(faces) > 0:
            last_face_detected_time = time.time()

        # Determine LED state
        current_time = time.time()
        if button_flag and last_face_detected_time and (current_time - last_face_detected_time <= 5):
            white_led.on()
        else:
            white_led.off()
            button_flag=False

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera.close()
    cv2.destroyAllWindows()
