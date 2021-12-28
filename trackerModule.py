import mediapipe as mp
import cv2

class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_conf=0.7,
                track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands,
                                        self.detection_conf, self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no = 0, draw = True, index=0):
        lm_list = 0
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            
            for id, lms in enumerate(my_hand.landmark):
                # print(id, lms)
                h, w, c = img.shape
                cx, cy = int(lms.x * w), int(lms.y * h)
                #print(id, cx, cy)
                lm_list = cx
                if id == index:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                    
        return lm_list
