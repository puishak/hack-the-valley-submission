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
        self.score = []
        self.repStarted = False
        self.checkAngle = 0
        self.tempLandMarks = None
        
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
                    self.score.append(checkScore(self.tempLandMarks))
                    self.count += 1
                    # calculate the score append it to self.score
                if hipAngle < self.checkAngle:
                    self.checkAngle = hipAngle
                    self.tempLandMarks = self.detector.lmlist
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
    
    def countRep(self,img):
        count = 0
        return 0
    
    # def checkScore(self,backPoint,depthPoint,kneePoint):
    #     score = 4 * backAngleScore(right[0], right[1])
    #     + 4 * depthScore(lmlist, right[1], right[2])
    #     + 2 * kneeScore(lmlist, right[2], right[5])
    
    
    
    # def backAngleScore(self,back, hip):
    #     backAngle = int(self.detector.angle_from_horizontal(hip,back))
    #     diff = abs((backAngle % 90)-45)
    #     if diff <= 45:
    #         return 1 - diff / 45
    #     else:
    #         return -1
        


    # if angle <= 45:
    #     score = np.interp(angle, (0, 45), (0, 1))
    # else:
    #     score = np.interp(angle, (90, 45), (0, 1))
        

def checkScore(lm):
    return 0

# def depthScore(eelf, lmlist, hip, knee):
#     _, hipY = lmlist[hip][1:]
#     _, kneeY = lmlist[knee][1:]
#     if hipY >= kneeY:
#         score = 1
#     else:
#         angle = int(self.detector.angle_from_horizontal(knee, hip))
#         score = np.interp(angle, (90, 0), (0, 1))
#     return score


# def kneeScore(lmlist, knee, foot):
#     kneeX, _ = lmlist[knee][1:]
#     footX, _ = lmlist[foot][1:]
#     if kneeX < footX:
#         return 1
#     else:
#         return 0
    
    
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

            print("count:", count, "; Progress:", int(progress*100))
            cv2.imshow("this could be decided at the last minute!!!", img)
            key = cv2.waitKey(1)
            if key == 32:
                break