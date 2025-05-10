# gesture.py
from cvzone.HandTrackingModule import HandDetector
import cv2

class GestureDetector:
    def __init__(self, maxHands=1):
        self.detector = HandDetector(maxHands=maxHands, detectionCon=0.7)

    def detect_gesture(self, frame):
        hands, img = self.detector.findHands(frame)
        if hands:
            hand = hands[0]
            fingers = self.detector.fingersUp(hand)

            # gestures:
            if fingers == [1, 1, 1, 1, 1]:
                return "OPEN"
            elif fingers == [0, 0, 0, 0, 0]:
                return "FIST"
            elif fingers == [0, 1, 0, 0, 0]:
                return "POINT"
            elif fingers == [0, 1, 1, 0, 0]:
                return "PEACE"
        return None
