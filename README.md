# Reaction and mobility Test
System to test mobility, muscle memory and reaction using OpenCV and mediapipe.

The main purpose of this project is apply the knowledge of digital image processing on a real life problem. The idea was to create a system that recognize a human hand and use it to touch objects that will appear randomly on the interface. Even though it appears to be simple, it is actually an extremelly usefull tool to help people in several ways, such as recovering pacients treatment, physical impaired people mobility development, etc.

![test](/img/testereacao.gif)

##How can we do this?

The first steps to start our project is import the necessary libraries.
We will use:
* mediapipe to detect the hands 
* OpenCV (cv2) to process the image, create the objects, create visuals and show them on screen.
* numpy
* time (to create the countdown system)
* random (to randomize the coordinates of the objects)

~~~Python
import mediapipe as mp
import cv2
import numpy as np
import time
import random
from scipy.spatial import distance as dist
~~~


