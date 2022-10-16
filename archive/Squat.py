import math
from operator import truediv
import cv2
import mediapipe as mp
import numpy as np
import poseModule as pm

detector = pm.poseDetector(mode=True)
right = [12, 24, 26, 28, 30, 32]

def update():
    detector.findPose(img, draw=False)
    lmlist, img = detector.findPosition(img, draw=False)

    if rep_started:
        # calculate shit
        pass

    if rep_bottom:
        reps.append(checkScore(lmlist))

        pass

    leg_angle = abs(detector.angle_from_horizontal(right[1], right[2]) - 90)
    print(leg_angle)
    if leg_angle > 10 and not rep_started:
        rep_started = True
    elif leg_angle <= 10 and rep_started:
        # print("rep:", len(reps))
        rep_started = False
    cv2.imshow("", img)
    key = cv2.waitKey(1)


def main():
    max = 2
    cap = cv2.VideoCapture(0)
    reps = []
    rep_started = False
    rep_bottom = False
    while len(reps) <= max:
        success, img = cap.read()

        if success:
            
            update()
            if key == 32:
                break
            # if repEnd():
            #     reps.append(checkScore(lmlist))

    # detector = pm.poseDetector(mode=True)
    # left = [11, 23, 25, 27, 29, 31]
    # right = [12, 24, 26, 28, 30, 32]
    # img = cv2.imread("test2.png")
    # detector.findPose(img, draw=False)
    # lmlist, img = detector.findPosition(img, draw=False)
    # angle, img = detector.findAngle(img, right[0], right[1], right[2])
    # angle2, img = detector.findAngle(img, right[2], right[3], right[4])
    # angle2, img = detector.findAngle(img, right[4], right[5], right[5])
    # result = detector.angle_from_horizontal(right[0], right[1])


def checkScore(lmlist):

    print("Back: ", backAngleScore(right[0], right[1]))
    print("Depth: ", depthScore(lmlist, right[1], right[2]))
    print("Knee: ", kneeScore(lmlist, right[2], right[5]))
    return (
        4 * backAngleScore(right[0], right[1])
        + 4 * depthScore(lmlist, right[1], right[2])
        + 2 * kneeScore(lmlist, right[2], right[5])
    )


def backAngleScore(back, hip):
    angle = 45
    # angle = int(detector.angle_from_horizontal(back, hip))
    # print(angle)
    # diff = math.abs(angle - 45)
    diff = abs(angle - 45)

    # if angle <= 45:
    #     score = np.interp(angle, (0, 45), (0, 1))
    # else:
    #     score = np.interp(angle, (90, 45), (0, 1))
    if diff <= 45:
        return 1 - diff / 45
    else:
        return -1


def depthScore(lmlist, hip, knee):
    hipX, hipY = lmlist[hip][1:]
    kneeX, kneeY = lmlist[knee][1:]
    if hipY >= kneeY:
        score = 1
    else:
        angle = int(detector.angle_from_horizontal(knee, hip))
        score = np.interp(angle, (90, 0), (0, 1))
    return score


def kneeScore(lmlist, knee, foot):
    kneeX, kneeY = lmlist[knee][1:]
    footX, footY = lmlist[foot][1:]
    if kneeX < footX:
        return 1
    else:
        return 0


def repStart():
    pass


def repEnd():
    pass


if __name__ == "__main__":
    # img = cv2.imread("test2.png")
    # detector.findPose(img, draw=False)
    # lmlist, img = detector.findPosition(img, draw=False)
    # print(checkScore(lmlist))

    main()
