from picamera import PiCamera
import time

camera= PiCamera()

camera.start_preview(alpha=200)
time.sleep(60)
camera.stop_preview()
