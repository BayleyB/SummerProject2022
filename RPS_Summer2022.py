import mediapipe as mp
import cv2
import numpy as np

mp_hand_drawing = mp.solutions.drawing_utils #Helps with drawing hand landmarks
mp_hands = mp.solutions.hands

mediaCap = cv2.VideoCapture(0) #set capture feed for webcam

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: #defining hand tracking as hands within the loop
    while mediaCap.isOpened():
        _, frame = mediaCap.read() #capture frame from webcam

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convert frame to RGB from BGR
        image.flags.writeable = False #Set Flag False
        detection = hands.process(image) #Make the hand detection
        image.flags.writeable = True #Set Flag True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #Convert image to BGR from RGB so that it can be rendered

        #List of finger tip landmarks for all fingers except the thumb
        finger_tip_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, 
                        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

        #Dictionary that will be used to detect if a finger is up or down in a captured frame, False will indicated finger is down, True will indicate it is up
        finger_up = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False, 'RIGHT_PINKY': False,
                    'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False, 'LEFT_RING': False, 'LEFT_PINKY': False}

        #If a hand was detected withing the captured frame, we want to draw it
        if detection.multi_hand_landmarks:
            for hand_index, hand in enumerate(detection.multi_handedness):
                
                #Label the hand as left or right
                hand_lr = hand.classification[0].label

                #Find the landmarks on the hand
                hand_landmarks = detection.multi_hand_landmarks[hand_index]

                #Loop throught the finger tip indexes
                for tip_index in finger_tip_ids:
                    finger_name = tip_index.name.split("_")[0] #Figure out which finger we are looking at first

                    #If the finger tip is higher than the midpoint, update the value to true in the dictionary
                    if (hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[tip_index-2].y):
                        finger_up[hand_lr.upper()+"_"+finger_name] = True
                
                #Get coordinates of tip and mcp landmarks on the thumb of the current hand
                thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP - 2].x

                #If the thumb is up, then set its value in the dictionary to true
                if (hand_lr=='Right' and (thumb_tip_x < thumb_mcp_x)) or (hand_lr=='Left' and (thumb_tip_x > thumb_mcp_x)):
                    finger_up[hand_lr.upper() + "_THUMB"] = True

                #Draw hand landmarks onto processed frame
                mp_hand_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if ((finger_up['RIGHT_THUMB'] == True and finger_up['RIGHT_INDEX'] == True and finger_up['RIGHT_MIDDLE'] == True and finger_up['RIGHT_RING'] == True and finger_up['RIGHT_PINKY'] == True) 
                or (finger_up['LEFT_THUMB'] == True and finger_up['LEFT_INDEX'] == True and finger_up['LEFT_MIDDLE'] == True and finger_up['LEFT_RING'] == True and finger_up['LEFT_PINKY'] == True)):
                    cv2.putText(image, "Paper", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 155), 2)
                elif ((finger_up['RIGHT_THUMB'] == False and finger_up['RIGHT_INDEX'] == False and finger_up['RIGHT_MIDDLE'] == False and finger_up['RIGHT_RING'] == False and finger_up['RIGHT_PINKY'] == False) 
                or (finger_up['LEFT_THUMB'] == False and finger_up['LEFT_INDEX'] == False and finger_up['LEFT_MIDDLE'] == False and finger_up['LEFT_RING'] == False and finger_up['LEFT_PINKY'] == False)):
                    cv2.putText(image, "Rock", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 155), 2)
                elif ((finger_up['RIGHT_INDEX'] == True and finger_up['RIGHT_MIDDLE'] == True and finger_up['RIGHT_RING'] == False and finger_up['RIGHT_PINKY'] == False) 
                or (finger_up['LEFT_INDEX'] == True and finger_up['LEFT_MIDDLE'] == True and finger_up['LEFT_RING'] == False and finger_up['LEFT_PINKY'] == False)):
                    cv2.putText(image, "Scissors", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 155), 2)
                else:
                    cv2.putText(image, "Choosing...", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 155), 2)

        cv2.imshow('Rock, Paper, Scissors', image) #show processed frame to user with hand landmarks

        if cv2.waitKey(10) & 0xFF == ord('q'): #pressing q will break from the loop and close out the window
            break

mediaCap.release() #next two lines close out window
cv2.destroyAllWindows()