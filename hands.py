import mediapipe as mp
import cv2
import numpy as np
import time
import random
from scipy.spatial import distance as dist


desenha = mp.solutions.drawing_utils
maos = mp.solutions.hands
cap = cv2.VideoCapture(0)
inicio = True

font = cv2.FONT_HERSHEY_SIMPLEX
position = (50, 50)
position_end = (180, 200)
fontScale = 1
color = (0, 0, 0)
thickness = 2
toques = 0
tocou = False
start= time.time()

with maos.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        acabou = False
        tempo = time.time() - start
        tempo_rest = 30 - tempo
        x = 0
        y = 0
        ret, frame = cap.read()
        height, width, channels = frame.shape
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                desenha.draw_landmarks(image, hand, maos.HAND_CONNECTIONS, 
                                        desenha.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2),
                                        desenha.DrawingSpec(color=(195, 195, 195), thickness=2, circle_radius=2),
                                         )
                x = int(hand.landmark[8].x*width)
                if x>=width:
                    x=width-1
                y = int(hand.landmark[8].y*height)
                if y>=height:
                    y=height-1                      
                cv2.circle(image, (x, y), 20, (0,255,255), 2)
      
            
        print()
        if(inicio == True):
            print("Inicio")
            centrox = random.randint(0,width)
            centroy = random.randint(0,height)
            inicio = False

        #print("(",x,", ",y,")")
        cv2.circle(image,(centrox,centroy), 50, (0,0,255), -1)

        D = dist.euclidean((x, y), (centrox, centroy))
        
        if D <= 45:
            centrox = random.randint(0,width)
            centroy = random.randint(0,height)
            toques = toques + 1

        texto = 'Toques: %(toques)s  Tempo restante: %(tempo)s' % {"toques":toques, "tempo": int(tempo_rest)}
        cv2.putText(image, texto, position, font, fontScale, color, thickness, cv2.LINE_AA)

        texto_end = "O tempo acabou!"
        if tempo_rest <= 1:
            cv2.putText(image, texto_end, position_end, font, 1, color, 3, cv2.LINE_AA)

        if tempo_rest <= 0:
            time.sleep(5.0)
            break

        cv2.imshow('Teste seus reflexos', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()