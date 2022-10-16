import cv2
import mediapipe as mp
import time
import math

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


class poseDetector:
    def __init__(
        self,
        mode=False,
        upper=False,
        smooth=True,
        complexity=1,
        detCon=0.5,
        trackCon=0.5,
    ):
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            mode,
            upper,
            complexity,
            smooth,
            detCon,
            trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils

    # def findPose(self, img, draw=True):
    #     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     self.results = self.pose.process(imgRGB)
    #     if self.results.pose_landmarks:
    #         if draw:
    #             mpDraw.draw_landmarks(
    #                 img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
    #             )
    #     return img

    def findPosition(self,img):
        self.img = img
        imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        self.lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                height, width, c = self.img.shape
                cx, cy = int(width * lm.x), int(height * lm.y)
                self.lmlist.append([cx, cy])
        return self.lmlist
    
    def draw(self,lm):
        if len(self.lmlist) == len(lm):
            mpDraw.draw_landmarks(
                    self.img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
        for i in range(len(lm) - 1):
            x1,y1 = self.lmlist[lm[i]][0:]
            x2,y2 = self.lmlist[lm[i+1]][0:]
            cv2.line(self.img, (x1, y1), (x2, y2), (255, 255, 255), 3) 
            cv2.circle(self.img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x1, y1), 15, (0, 0, 255), 2)
            if i == (len(lm) - 2):
                cv2.circle(self.img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
                cv2.circle(self.img, (x2, y2), 15, (0, 0, 255), 2)
        return self.img
        
    def findAngle(self, p1, p2, p3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = self.lmlist[p3][1:]

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        )
        if angle <= 0:
            angle += 360
        # if draw:
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        #     cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
        #     cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        #     cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
        #     cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        #     cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
        #     cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
        #     cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)
        #     cv2.putText(
        #         img,
        #         f"{int(angle)} degrees",
        #         (x2 - 20, y2 - 50),
        #         cv2.FONT_HERSHEY_PLAIN,
        #         2,
        #         (0, 0, 0),
        #         2,
        #     )
        return angle

    def angle_from_horizontal(self, p1, p2) -> float:
        x1, y1 = self.lmlist[p1][0:]
        x2, y2 = self.lmlist[p2][0:]
        x3, y3 = x1,y2

        angle = math.degrees(
            math.atan2(y1 - y2, x2 - x1)
        )
        return angle
     
    
    
if __name__ == "__main__":
    import cv2
    
    cameraInput = cv2.VideoCapture(0)
    while True:
        success, img = cameraInput.read()
        if success:
            
            detector = poseDetector()
                    
            lm = detector.findPosition(img)
            if len(lm) != 0:
                img = detector.draw([13, 15])
                angle = detector.angle_from_horizontal(13,15)
                print(angle)
            cv2.imshow("this could be decided at the last minute!!!", img)
            key = cv2.waitKey(1)
            if key == 32:
                break