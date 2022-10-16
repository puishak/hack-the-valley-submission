import cv2
import time
import poseModule as pm
import numpy as np


cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count = 0
dir = 0
while True:
    suc, img = cap.read()
    if suc:
        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, draw=False)
        lmlist, img = detector.findPosition(img, draw=False)
        if len(lmlist) != 0:
            angle, img = detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (50, 120), (100, 0))
            bar = np.interp(per, (0, 100), (400, 150))

            if per == 0:
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 100:
                if dir == 1:
                    count += 0.5
                    dir = 0

            cv2.rectangle(img, (1220, 150), (1260, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (1220, int(bar)), (1260, 400), (0, 255, 0), cv2.FILLED)

            cv2.putText(
                img,
                f"{int(per)}%",
                (40, 450),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 0),
                3,
            )
            cv2.rectangle(img, (20, 555), (170, 700), (0, 255, 0), cv2.FILLED)
            cv2.putText(
                img,
                str(int(count)),
                (45, 675),
                cv2.FONT_HERSHEY_PLAIN,
                10,
                (255, 0, 0),
                25,
            )
        cv2.imshow("", img)
        key = cv2.waitKey(1)
        if key == 32:
            break
        continue
    break
