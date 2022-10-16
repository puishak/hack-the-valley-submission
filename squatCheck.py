from turtle import right
import cv2
import mediapipe as mp
import PoseModule as pm
import numpy as np

THRESHOLD = 0.2
RIGHT = [11,23,25,29,31]
LEFT = [12,24,26,30,32]

class SquatCheck:
    def __init__(self) -> None:
        self.angleTrack = []
        self.direction = False # False means down
        self.detector = pm.poseDetector()
        self.count = 0
        self.scores = []
        self.repStarted = False
        self.checkAngle = 0
        self.tempScore = None
        
    def check(self,img):
        # output [img(count,landmarks,progressbar), count, progress]
        self.detector.findPosition(img)
        if len(self.detector.lmlist)!=0:
            hipAngle = int(self.detector.angle_from_horizontal(25,23))
            # print(hipAngle)
            progress = np.interp(hipAngle, (0, 90), (1, 0))
            
            if self.repStarted:
                if progress < THRESHOLD:
                    self.repStarted = False
                    self.scores.append(self.tempScore)
                    self.count += 1
                    
                if hipAngle < self.checkAngle:
                    self.checkAngle = hipAngle
                    self.tempScore = self.checkScore()
            else:
                if progress > THRESHOLD:
                    self.repStarted = True
                    
            img = self.detector.draw(RIGHT)
            return img, self.count, progress
        else:
            return img, self.count, 0
            # bar = np.interp(self.progress, (0, 100), (400, 150))

    def getScore(self):
        return self.getScore
    
    def checkScore(self):
        return 4 * self.backAngleScore() + 4 * self.depthScore() + 2 * self.kneeScore()
    
    def backAngleScore(self):
        backAngle = int(self.detector.angle_from_horizontal(RIGHT[1],RIGHT[0]))
        diff = abs((backAngle % 90)-45)
        if diff <= 45:
            return 1 - diff / 45
        else:
            return -1
    
    def depthScore(self):
        _, hipY = self.detector.lmlist[RIGHT[1]]
        _, kneeY = self.detector.lmlist[RIGHT[2]]
        if hipY >= kneeY:
            score = 1
        else:
            angle = int(self.detector.angle_from_horizontal(RIGHT[2], RIGHT[1]))
            score = np.interp(angle, (90, 0), (0, 1))
        return score
    
    def kneeScore(self):
        kneeX, _ = self.detector.lmlist[RIGHT[2]]
        footX, _ = self.detector.lmlist[RIGHT[4]]
        if kneeX < footX:
            return 1
        else:
            return 0
    
    
if __name__ == "__main__":
    import cv2
    
    cameraInput = cv2.VideoCapture(0)
    
    squat1 = SquatCheck()
    while True:
        success, img = cameraInput.read()
        if success:
            img = cv2.flip(img, 1)
            img, count, progress = squat1.check(img)
            cv2.rectangle(img, (20, 55), (120, 155), (0, 255, 0), cv2.FILLED)
            cv2.putText(
                img,
                str(count),
                (30, 105),
                cv2.FONT_HERSHEY_PLAIN,
                8,
                (255, 255, 255),
                6,
            )

            # print("count:", count, "; Progress:", int(progress*100))
            print(squat1.scores)
            cv2.imshow("this could be decided at the last minute!!!", img)
            key = cv2.waitKey(1)
            if key == 32:
                break