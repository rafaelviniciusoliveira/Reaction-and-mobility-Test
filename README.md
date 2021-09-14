# Reaction and mobility Test
System to test mobility, muscle memory and reaction using OpenCV and mediapipe.

The main purpose of this project is to apply the knowledge of digital image processing on a real life problem. The idea was to create a system that recognize a human hand and use it to touch objects that will appear randomly on the interface. Even though it appears to be simple, it is actually an extremelly usefull tool to help people in several ways, such as recovering pacients treatment, physical impaired people mobility development, etc.

![test](/img/gif.gif)

## How can we do this?

The first steps to start our project is import the necessary libraries.
We will use:
* mediapipe to detect the hands 
* OpenCV (cv2) to process the image, create the objects, create visuals and show them on screen.
* numpy
* time (to create the countdown system)
* random (to randomize the coordinates of the objects)
* distance from scipy.spatial to calculate the euclidean distance between points

~~~Python
import mediapipe as mp
import cv2
import numpy as np
import time
import random
from scipy.spatial import distance as dist
~~~

The next step is declaire the initial objects responsible for the drawing and the detection of the human hands. Also, we declaire the variable cap, that will receive the image from the webcam.

~~~Python
desenha = mp.solutions.drawing_utils
maos = mp.solutions.hands
cap = cv2.VideoCapture(0)
~~~

Finishing the inicialization process, we define the initial positions, colors, fonts and other objects particulars.   

~~~Python
font = cv2.FONT_HERSHEY_SIMPLEX
position = (50, 50)
position_end = (180, 200)
fontScale = 1
color = (0, 0, 0)
thickness = 2
~~~

Before we start the loop and the test itself, were created three variables to store the number of touches, show if the object was touched and to start counting the time, respectively. 

~~~Python
toques = 0
tocou = False
start= time.time()
~~~

Now, we start our detection defining the minimum detection confidence and the minimum tracking confidence. And while  frames are being captured:

* The image configurations are set and the image is processed.

~~~Python
ret, frame = cap.read()
height, width, channels = frame.shape
image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image = cv2.flip(image, 1)
image.flags.writeable = False
results = hands.process(image)
image.flags.writeable = True
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
~~~

* The hand points and the hand connections are drawn, the coordinates of the tip of the index finger is collected and a circle is drawn on it. That's the base point to check if the hand touches the object.

~~~Python
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
~~~

* The first object is rendered using random coordinates.

~~~Python
if(inicio == True):
            print("Inicio")
            centrox = random.randint(0,width)
            centroy = random.randint(0,height)
            inicio = False

cv2.circle(image,(centrox,centroy), 50, (0,0,255), -1)
~~~

* The euclidean distance between the center of the object and the tip of the index finger is taken. If the finger is inside the area of the object, a new random position in given and the number of touches increases.

~~~Python
D = dist.euclidean((x, y), (centrox, centroy))
if D <= 45:
            centrox = random.randint(0,width)
            centroy = random.randint(0,height)
            toques = toques + 1
~~~

* The number of touches and the remaining time are always shown.

~~~Python
texto = 'Toques: %(toques)s  Tempo restante: %(tempo)s' % {"toques":toques, "tempo": int(tempo_rest)}
cv2.putText(image, texto, position, font, fontScale, color, thickness, cv2.LINE_AA)
~~~

* The image is shown until the time is over or "q" is pressed.
~~~Python
texto_end = "O tempo acabou!"
if tempo_rest <= 1:
            cv2.putText(image, texto_end, position_end, font, 1, color, 3, cv2.LINE_AA)

if tempo_rest <= 0:
            time.sleep(5.0)
            break
            
cv2.imshow('Teste seus reflexos', image)
if cv2.waitKey(10) & 0xFF == ord('q'):
            break
~~~

At the end, the cap is released and the windows are destroyed.

~~~Python
cap.release()
cv2.destroyAllWindows()
~~~

## Complete code:

~~~Python
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
      
        if(inicio == True):
            print("Inicio")
            centrox = random.randint(0,width)
            centroy = random.randint(0,height)
            inicio = False

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
~~~
