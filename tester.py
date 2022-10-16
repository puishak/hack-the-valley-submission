import cv2
import numpy

def main():
    cameraInput = cv2.VideoCapture(0)
    while True:
        success, img = cameraInput.read()
        if success:
            img = cv2.flip(img, 1)
            # flip img
            img = cv2.resize(img, (1280, 720))
            # 
            key = cv2.waitKey(1)