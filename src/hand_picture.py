import sys
import os

import cv2
import mediapipe as mp
import pandas

import hand as hd
import hand_plot as hd_plt

if len(sys.argv) != 3:
  print('Error en los argumentos')
  quit()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

IMAGE_FILES = []
data_set = pandas.DataFrame()

direc = sys.argv[1]
for folder in os.listdir(direc):
  fold = os.path.join(direc,folder)
  c = 0
  for image in os.listdir(fold):
    f = os.path.join(fold,image)
    if os.path.isfile(f):
      IMAGE_FILES.append(f)
      c = c + 1
      if c == 200:
        break

print(len(IMAGE_FILES))

# For static images:
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        hand = hd.Hand(hand_landmarks)
        features = hand.bezier_curve_features()
        features['gesture'] = file.split('/')[3][-1]
        data_set = pandas.concat([data_set, features])
        print(len(data_set.index))
        
        #print(len(hand.bezier_curve_features()))
        #print(hand.bezier_curve_features())
        #hd_plt.HandPlot(hand).plot() #PLOT

data_set.to_csv(sys.argv[2])

# python3 src/hand_picture.py ../datasets-tesis/Hagrid/ features_call.csv
