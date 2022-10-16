
from Challenge import Challenge
from squatCheck import SquatCheck
import cv2
import numpy as np

TARGET_REPS = 10

class ClassicChallange(Challenge):
    
    def __init__(self) -> None:
        super().__init__()
        self.squat = SquatCheck()
        self.started = True
        
    
    def update(self, img):
        
        if self.started:
            img, count, progress = self.squat.check(img)
            
            
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
            
            #Draw progress bar on the image
            cv2.rectangle(img, (1220, 150), (1260, 400), (0, 255, 0), 3)
            bar = np.interp(progress, (0, 100), (400, 150))
            cv2.rectangle(img, (1220, bar), (1260, 400), (0, 255, 0), cv2.FILLED)
            
            if count >= TARGET_REPS:
                self.started = False
        else:
            # Calculate total scores, and show end screen
            score = self.squat.getScore()

        return img

