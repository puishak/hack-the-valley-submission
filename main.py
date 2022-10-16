import cv2 as cv
import numpy as np
from TimeAttackChallange import TimeAttackChallange
from  ClassicChallange import ClassicChallange
from Challenge import Challenge


ch = None

def main():
    challengeStarted = False
    cap = cv.VideoCapture(0)
    
    
    rootWindow = "this could be decided at the last minute!!!"
    cv.namedWindow(rootWindow)
    
    while True:
        success, img = cap.read()
        if success:
            img = cv.flip(img, 1)
            # flip img
            img = cv.resize(img, (1280, 720))
            # 
            key = cv.waitKey(1)

            if challengeStarted:
                img = ch.update(img)
            else:
                # Show text - "Press 'c' for Classic challenge, and 't' for a time attack challenge"
                #cv.displayOverlay(rootWindow, "Press 'c' for Classic challenge, and 't' for a time attack challenge")
                if key == ord('c'):
                    print("Classic Challange!")
                    ch = ClassicChallange()
                    challengeStarted = True
                    
                if key == ord('t'):
                    print("Time Attack Challange!")
                    ch = TimeAttackChallange()
                    challengeStarted = True
                
                
                

            # Output
            cv.imshow(rootWindow, img)
            # UI button for exit
            if key == 32:
                break
    
    cv.destroyAllWindows()
    

# def onClassicChallangeButton(*args):
#     # Classic Challange button has been pressed

# def onTimeAttackChallangeButton(*args):
#     # Classic Challange button has been pressed
#     print("Time Attack Challange")
#     challenge = TimeAttackChallange()
#     challengeStarted = True


# def onMouseEvent(event, x, y, flags, param):
#     if event == cv.EVENT_LBUTTONUP:
#         pass
    


        

    
if __name__ == "__main__":
    main()