import cv2  
import mediapipe as mp  

class HandTracker:  
    def __init__(self):  
        self.mp_hands = mp.solutions.hands  
        self.hands = self.mp_hands.Hands(  
            static_image_mode=False,  
            max_num_hands=1,  
            min_detection_confidence=0.8, 
            min_tracking_confidence=0.8  
        )  
        self.mp_drawing = mp.solutions.drawing_utils  
        
    def get_finger_position(self, frame):  
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        results = self.hands.process(frame_rgb)  
        
        if results.multi_hand_landmarks:  
            for hand_landmarks in results.multi_hand_landmarks:  
                self.mp_drawing.draw_landmarks(  
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS  
                )  
                # PULGAR (landmark 4)  
                thumb = hand_landmarks.landmark[4]  
                h, w, _ = frame.shape  
                x, y = int(thumb.x * w), int(thumb.y * h)  
                # Círculo ROJO para el pulgar  
                cv2.circle(frame, (x, y), 20, (0, 0, 255), -1)  
                return (x, y)  
        return None  