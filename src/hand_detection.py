import mediapipe as mp


class HandDetection:
    def __init__(self, num_hands=1):
        self.mp_hands = mp.solutions.hands.Hands(max_num_hands=num_hands)
        self.num_hands = num_hands

    def get_hand_landmarks(self, image):
        results = self.mp_hands.process(image)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks
        return None

    def get_multi_handedness(self, image):
        results = self.mp_hands.process(image)
        if results.multi_handedness:
            return results.multi_handedness
        return None

    def get_hand_info(self, image):
        results = self.mp_hands.process(image)
        if results.multi_hand_landmarks and results.multi_handedness:
            return results.multi_hand_landmarks, results.multi_handedness
        return None, None
