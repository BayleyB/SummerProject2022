# README for Rock, Paper, Scissors using MediaPipe

**Last Updated: 9/8/2022**

**Basic Description:**

This program uses MediaPipe's machine learning API as well as OpenCV's computer vision library to recognize hand gestures in a Rock, Paper, Scissors game. The player plays against a computer that chooses Rock, Paper, or Scissors and compares it to the player's choice and determines a winner.

**Files:**

The following is a list of files in the project folder and a description of them.

**Code Files:**
- rps.py: This is the main code file for the program, it also contains customizable parameters so that the user can modify various aspects of the appearence of the game.
- game.py: This file contains the code for the Rock, Paper, Scissors game.
- menu_resources.py: File with currently a single function that is used to display some about information about the game.

**Extra Files:**
- README: Contains program description, file description, usage, and information referenced in the creation of this program.

**Usage:**
- Install mediapipe, cv2, and PySimpleGUI package.
- Run rps.py file which will bring up the main menu for the game, from there follow the prompts on the screen.

**References:**

The following sources were referenced in the creation of this program. A short description of why they were referenced is below each source.

**MediaPipe Hands Docs**

https://google.github.io/mediapipe/solutions/hands.html
This is the docs for MediaPipe's hand recognition solution used in the creation of the game. This API has the ability to recognize the position of various different landmarks on the users hand which I utilized in recognizing hand gestures.

**AI Hand Pose Estimation**

https://www.youtube.com/watch?v=vQZ4IvB07ec
I referenced this video when making my gesture recognition algorithm, that uses the positions of various hand lankmarks in a frame to estimate which hand gesture the user is attempting to show.

**Real-Time Fingers Counter & Hand Gesture Recognizer**

https://www.youtube.com/watch?v=epwlqHHbELE
I referenced this video as well in creating the algorithm to recognize Rock, Paper, Scissors gestures.

**PySimpleGui Docs**

https://www.pysimplegui.org/en/latest/readme/
This was referenced when learning how to use the PySimpleGUI framework when creating the GUI for the game.