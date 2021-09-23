import sys
import cv2
import mediapipe as mp
import numpy as np

def main():
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands
  # input
  cap = cv2.VideoCapture('https://r1---sn-9gv7enek.googlevideo.com/videoplayback?expire=1632362290&ei=0opLYeXdN9Gw2_gP9q6YgAM&ip=189.217.10.25&id=o-ANjZcCZNnmgPkIP48XAoQqkcn5F4NoCKnOdeUUPbqmkV&itag=22&source=youtube&requiressl=yes&vprv=1&mime=video%2Fmp4&ns=nA8octP7VXehUrCR7NuB4l8G&cnr=14&ratebypass=yes&dur=90.975&lmt=1579996493225742&fexp=24001373,24007246&c=WEB&txp=1306222&n=Z06NDK6nIcR_gGQm&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAMN_lXxiqONlpxf5TZl2B7yimIWTi-vN8EvRH4_nbgZOAiEArSmN6JIJpRYEu-t1B-GsHKHVr4JNm0Y5I8pubVOrl5A%3D&redirect_counter=1&cm2rm=sn-j5cax8pnpvohm-hxmz7k&req_id=bfa1716aad98a3ee&cms_redirect=yes&mh=pu&mm=29&mn=sn-9gv7enek&ms=rdu&mt=1632341356&mv=m&mvi=1&pl=22&lsparams=mh,mm,mn,ms,mv,mvi,pl&lsig=AG3C_xAwRQIgUYu5ee762knmkRf-D1TeBNEJo7y689k2NDRI-AEVRuoCIQCLgNLEz-2h0-p1G2jo1oaEM5oG0ZQwUfuw30xko1MsUQ%3D%3D')
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
