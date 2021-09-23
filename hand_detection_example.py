import sys
import cv2
import mediapipe as mp
import numpy as np

def main():
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands
  # input
  cap = cv2.VideoCapture('Video URL')
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))
  # output
  out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 
                          30, (frame_width,frame_height))
  
  hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Create blank image
    blank_image = np.zeros((frame_height,frame_width,3), np.uint8)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
          blank_image,
          hand_landmarks, # Las coordenadas de los 21 puntos de la mano
          mp_hands.HAND_CONNECTIONS, # La relacion de las 21 coordenadas
          mp_drawing_styles.get_default_hand_landmarks_style(), # Los colores y estilos de los 21 puntos
          mp_drawing_styles.get_default_hand_connections_style()) # Los colores y estilos de las conexiones
    # cv2.imshow('MediaPipe Hands', image)
    # Save video to file
    
    out.write(blank_image)

    if cv2.waitKey(5) & 0xFF == 27:
      break
  
  cap.release()
  out.release()

  cv2.destroyAllWindows()

main()
