import mediapipe as mp
import cv2
import random

font = cv2.FONT_HERSHEY_COMPLEX

def run_game():
    mp_hand_drawing = mp.solutions.drawing_utils #Helps with drawing hand landmarks
    mp_hands = mp.solutions.hands

    mediaCap = cv2.VideoCapture(0) #Set capture feed for webcam

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: #defining hand tracking as hands within the loop
        while mediaCap.isOpened():
            #Capture frame from webcam
            _, frame = mediaCap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            detection = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            #List of finger tip landmarks for all fingers except the thumb
            finger_tip_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, 
                            mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

            #Used to keep track of # of fingers up on each hand
            finger_count = {'LEFT': 0, 'RIGHT': 0}

            #Dictionary that will be used to detect if a finger is up or down in a captured frame, False will indicated finger is down, True will indicate it is up
            finger_up = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False, 'RIGHT_PINKY': False,
                        'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False, 'LEFT_RING': False, 'LEFT_PINKY': False}

            #Keeps track of choice for the player and computer to determine a winner
            player_choice = 'Choosing...'
            comp_choice = 'Choosing...'

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
                            finger_count[hand_lr.upper()] += 1
                    
                    #Get coordinates of tip and mcp landmarks on the thumb of the current hand
                    thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                    thumb_mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP - 2].x

                    #If the thumb is up, then set its value in the dictionary to true
                    if (hand_lr=='Right' and (thumb_tip_x < thumb_mcp_x)) or (hand_lr=='Left' and (thumb_tip_x > thumb_mcp_x)):
                        finger_up[hand_lr.upper() + "_THUMB"] = True
                        finger_count[hand_lr.upper()] += 1

                    #Draw hand landmarks onto processed frame
                    mp_hand_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_hand_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

                    #Hand gesture recognition utilizing knowledge of what hand is observed
                    if (finger_up[hand_lr.upper() + '_INDEX'] and finger_up[hand_lr.upper() + '_MIDDLE'] and finger_count[hand_lr.upper()] == 2):
                        player_choice = 'Scissors'
                    elif (finger_count[hand_lr.upper()] == 5):
                        player_choice = 'Paper'
                    elif (finger_count[hand_lr.upper()] == 0):
                        player_choice = 'Rock'
                    else:
                        player_choice = 'Choosing...'

            cv2.putText(image, player_choice, (10, 25), font, 1, (255, 0, 0), 2)

            #Determine whether the player wins, loses, or ties
            if (cv2.waitKey(10) & 0xFF == ord(' ')) and player_choice != 'Choosing...':
                comp_choice_num = random.randint(1, 3)
                if(comp_choice_num == 1):
                    comp_choice = 'Scissors'
                elif(comp_choice_num == 2):
                    comp_choice = 'Paper'
                elif(comp_choice_num == 3):
                    comp_choice = 'Rock'
                cv2.putText(image, comp_choice, (475, 25), font, 1, (0, 0, 255), 2)

                if ((player_choice == 'Scissors' and comp_choice == 'Paper') 
                or (player_choice == 'Paper' and comp_choice == 'Rock')
                or (player_choice == 'Rock' and comp_choice == 'Scissors')):
                    cv2.putText(image, 'WINNER', (125, 200), font, 3, (20, 255, 155), 2)
                elif (player_choice == comp_choice):
                    cv2.putText(image, 'TIE', (225, 200), font, 3, (0, 230, 255), 2)
                else:
                    cv2.putText(image, 'YOU LOSE', (75, 200), font, 3, (0, 0, 255), 2)

                cv2.putText(image, 'Press any key to continue...', (75, 300), font, 1, (255, 255, 255), 2)
                cv2.imshow('Rock, Paper, Scissors', image)
                cv2.waitKey(0)

            cv2.putText(image, 'Press Space to lock in choice', (10, 400), font, 1, (255, 255, 255), 2)
            cv2.putText(image, 'Press Q to exit game', (10, 450), font, 1, (255, 255, 255), 2)
            cv2.imshow('Rock, Paper, Scissors', image)

            #Pressing q will break from the loop and close out the window
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    mediaCap.release()
    cv2.destroyAllWindows()
    return