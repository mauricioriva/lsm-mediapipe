import math
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pulgar_x = 0
pulgar_y = 0
pulgar_z = 0

def get_distancia(x1,y1,z1,x2,y2,z2):
  return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def get_distancia_pulgar(x,y,z):
  return get_distancia(x,y,z,pulgar_x,pulgar_y,pulgar_z)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Dibuja marcas en la imagen
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        # Obten distancia del punto 18 al 20
        px_18 = hand_landmarks.landmark[18].x
        py_18 = hand_landmarks.landmark[18].y
        pz_18 = hand_landmarks.landmark[18].z
        
        px_20 = hand_landmarks.landmark[20].x 
        py_20 = hand_landmarks.landmark[20].y
        pz_20 = hand_landmarks.landmark[20].z
        
        #d_ref = get_distancia(px_18, py_18, pz_18, px_20, py_20, pz_20)
        
        d_ref = 0.18

        # Prints
        #print('=======  17  =======')
        #print(hand_landmarks.landmark[17])
        #print('=======  20  =======')
        #print(hand_landmarks.landmark[20])
        #print('=======  D  =======')
        #print(d_ref)

        pulgar_x = hand_landmarks.landmark[4].x
        pulgar_y = hand_landmarks.landmark[4].y
        pulgar_z = hand_landmarks.landmark[4].z

        px_8 = hand_landmarks.landmark[8].x 
        py_8 = hand_landmarks.landmark[8].y
        pz_8 = hand_landmarks.landmark[8].z
        
        px_12 = hand_landmarks.landmark[12].x 
        py_12 = hand_landmarks.landmark[12].y
        pz_12 = hand_landmarks.landmark[12].z

        px_16 = hand_landmarks.landmark[16].x 
        py_16 = hand_landmarks.landmark[16].y
        pz_16 = hand_landmarks.landmark[16].z

        d1 = get_distancia_pulgar(px_8, py_8, pz_8)
        d2 = get_distancia_pulgar(px_12, py_12, pz_12)
        d3 = get_distancia_pulgar(px_16, py_16, pz_16)
        d4 = get_distancia_pulgar(px_20, py_20, pz_20)

        if d1 < d_ref and d2 < d_ref and d3 < d_ref and d4 < d_ref:
          print("Closed")
        else:
          print("Open")

        print(hand_landmarks.landmark[0].x)
        print(hand_landmarks.landmark[0].y)
        print(hand_landmarks.landmark[0].z)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
