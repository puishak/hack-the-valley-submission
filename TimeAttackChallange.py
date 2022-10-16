import time
from Challenge import Challenge
from squatCheck import SquatCheck
import cv2

DURATION = 40 #seconds


class TimeAttackChallange(Challenge):
    
    
    
    def __init__(self) -> None:
        self.squat = SquatCheck()
        self.started = True
        self.startTime = time.time()
        
        super().__init__()
    
    def update(self, img):
        
        elapsedTime = time.time() - self.startTime
        
        if self.started:
            img, count, progress = self.squat.check(img)
            
            # cv2.putText(img, count, )
            # Draw count
            cv2.rectangle(img, (20, 555), (170, 700), (0, 255, 0), cv2.FILLED)
            cv2.putText(
                img,
                str(count),
                (45, 675),
                cv2.FONT_HERSHEY_PLAIN,
                10,
                (255, 0, 0),
                25,
            )

            # Draw the time
            countDown = (int)(DURATION - elapsedTime)
            cv2.rectangle(img, (20, 555), (170, 700), (0, 255, 0), cv2.FILLED)
            cv2.putText(
                img,
                str(countDown),
                (45, 675),
                cv2.FONT_HERSHEY_PLAIN,
                10,
                (255, 0, 0),
                25,
            )
            
            # Draw progress bar on the image
            # cv2.rectangle(img, (1220, 150), (1260, 400), (0, 255, 0), 3)
            # cv2.rectangle(img, (1220, progress * 100), (1260, 400), (0, 255, 0), cv2.FILLED)

            
            
            if elapsedTime > DURATION:
                self.started = False
        else:
            # Calculate total scores, and show end screen
            score = self.squat.getScore()

        return img