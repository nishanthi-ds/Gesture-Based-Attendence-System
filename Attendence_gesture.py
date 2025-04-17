import cv2, math
import mediapipe as mp

# Finger landmark mapping in MediaPipe:
# 0: Wrist
# 1-4: Thumb (1: base → 4: tip)
# 5-8: Index Finger
# 9-12: Middle Finger
# 13-16: Ring Finger
# 17-20: Pinky

# === Step 1: Initialize MediaPipe Hands model ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# === Step 2: Start webcam feed ===
cap = cv2.VideoCapture(0)

# === Step 3: Function to recognize hand gestures ===
def is_close(point1, point2, threshold=0.1):
    """Euclidean distance."""
    distance = math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    return distance < threshold

def get_gesture(landmarks):
    # Tip landmark indices for each finger
    tips = [4, 8, 12, 16, 20]

    fingers = []

    # Thumb logic:
    # If tip (4) is to the left of joint (3), it's extended (for right hand)
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index to pinky fingers:
    # If tip is above the joint below it (tip.y < joint.y), it's extended
    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    close_count = 0
    for i in tips[1:]:  # skip thumb (already taken)
        if is_close(landmarks[4], landmarks[i],threshold=0.1):
            close_count += 1

    # Interpret the hand gesture based on finger states
    if close_count >= 3 and fingers  == [1, 1, 1, 1, 1] :
        return "Break-In"      # eat gesture
    elif fingers == [1, 1, 1, 1, 1]:
        return "Start"         # Open palm
    elif fingers == [0, 0, 0, 0, 0]:
        return "Stop"          # Closed fist
    elif fingers[1:] == [0, 1, 1,1] and is_close( handLms.landmark[4], handLms.landmark[8],threshold=0.1):
        return "Break-Out"     # super gesture

    return "None"

# === Step 4: Main loop to process video frames ===
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR (OpenCV) to RGB (MediaPipe expects RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    result = hands.process(rgb)

    gesture_text = "No Hand Gesture Detected"

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            # Draw landmarks and connections
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            #Loop through each landmark to draw and label
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Draw small circle at each landmark point
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                # # Label each point with its ID
                # cv2.putText(frame, str(id), (cx + 5, cy + 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # Recognize gesture from landmarks
            gesture = get_gesture(handLms.landmark)
            if gesture != "None":
                gesture_text = gesture

    # Show detected gesture on screen
    cv2.putText(frame, gesture_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,215,0), 2)

    # Display the frame
    cv2.imshow("Attendence Gesture", frame)

    # Quit the app by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Step 5: Release resources ===
cap.release()
cv2.destroyAllWindows()




