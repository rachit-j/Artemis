# gesture.py
import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils

    def detect_gesture(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                landmarks = hand.landmark
                # Simple trigger gesture: Open palm (index + middle finger extended)
                if landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y:
                    return "ACTIVATE"
        return None
