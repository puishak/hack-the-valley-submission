import cv2
import mediapipe as mp
import time
import handmodule as hm
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

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
        return img

    def findPosition(self, img, draw=True):
        self.lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                height, width, c = img.shape
                cx, cy = int(width * lm.x), int(height * lm.y)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return self.lmlist, img

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = self.lmlist[p3][1:]

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        )
        if angle <= 0:
            angle += 360
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
            cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)
            cv2.putText(
                img,
                f"{int(angle)} degrees",
                (x2 - 20, y2 - 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 0),
                2,
            )
        return angle, img

    def angle_from_horizontal(self, lm1, lm2) -> float:
        x1, y1 = self.lmlist[lm1][1:]
        x2, y2 = self.lmlist[lm2][1:]
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return (180 - angle) % 90


def main():

    cap = cv2.VideoCapture(0)
    pTime = 0
    detect = poseDetector()
    hand = hm.handDetector()
    while True:
        success, img = cap.read()
        # Fps calculation and show
        # img = hand.findHands(img)
        img = detect.findPose(img, draw=False)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        lmlist, img = detect.findPosition(img, draw=False)
        if len(lmlist) != 0:
            print(lmlist[16])
            cv2.circle(img, (lmlist[16][1], lmlist[16][2]), 5, (0, 0, 255), 2)
        cv2.putText(
            img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        )
        cv2.imshow("", img)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()
