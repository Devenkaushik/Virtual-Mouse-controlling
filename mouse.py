import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui
import time
import threading
import sys

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=1,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

def move_cursor(wScr, clocX, clocY):
    pyautogui.moveTo(wScr - clocX, clocY)

def start_thread(wScr, clocX, clocY): 
    thread = threading.Thread(target=move_cursor, args=(wScr, clocX, clocY))
    if not thread.is_alive():
        thread.start()

def zoom_out():
    pyautogui.hotkey('ctrl', '-')
    

def zoom_in():
    pyautogui.hotkey('ctrl', '+')

def main():
    # Define screen dimensions
    wCam, hCam = 640, 480
    frameR = 100  # Frame Reduction
    smoothening = 5
    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    
    prvs_length = 0

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    # Initialize hand detector
    detector = handDetector(maxHands=1)
    wScr, hScr = pyautogui.size()  # Get screen size

    # tranking of "if mouse clicked or not"
    r_clicked = ""
    l_clicked = ""

    try:
        while True:
            # Capture frame from webcam
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                # Check which fingers are up
                fingers = detector.fingersUp()
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                # Only Index Finger: Moving Mode
                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    start_thread(wScr, clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                # Both Index and Middle Fingers Up: Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1:
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        if not l_clicked:
                            pyautogui.click()
                            l_clicked = True
                        else:
                            l_clicked = False
                
                if fingers[0] == 1 and fingers[1] == 0:
                    length, img, lineInfo = detector.findDistance(4, 12, img)
                    if length < 40 :
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        if not r_clicked:
                            pyautogui.click(button='right')
                            r_clicked = True
                    else:
                        r_clicked = False

                if fingers[0] == 1 and fingers[1] == 1:
                    length, img, lineInfo = detector.findDistance(4, 8, img)
                    change_in_length = length - prvs_length
                    if  30 > change_in_length > 10 :  # Close together
                        zoomIN = threading.Thread(target=zoom_in)
                        if not zoomIN.is_alive():
                            zoomIN.start()  # Zoom in

                    elif -10 > change_in_length > -30 :  # Far apart
                        zoomOUT = threading.Thread(target=zoom_out)
                        if not zoomOUT.is_alive():
                            zoomOUT.start()  # Zoom out

                    prvs_length = length
                
            # Mirror the image for better hand eye co_ordination.
            img = cv2.flip(img, 1)

            # Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            window_name = "Always on Top Window"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            cv2.resizeWindow(window_name, wCam, hCam)  

            # Display the image
            cv2.imshow(window_name, img)
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                cap.release()  # Release the webcam
                cv2.destroyAllWindows()
                sys.exit("\n\nPLEASE SHARE YOUR EXPERIENCE WITH THE DEVELOPER  :)\n or any suggestion?\n")
    finally:
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows
        

if __name__ == "__main__":
    print("""\n\nIMPORTANT MESSAGE FOR EVERYONE:\n
          This project is currently in the alpha stage.
          If you are not familiar with Python, please ignore the console output.
          If you encounter any errors, contact the developer.
          Have an idea? Reach out to the developer to help implement it.
          If you are a developer, contributions are welcome!

          LAST BUT NOT THE LEAST:
          Please do not expect fluid functionality at this point of development as it is still in the alpha stage.\n""")
    main()
