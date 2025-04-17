import cv2, math, csv
import mediapipe as mp
from datetime import datetime

# === Initialize MediaPipe Hands model ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# === Start webcam feed ===
cap = cv2.VideoCapture(0)

# === Initialize CSV logging ===
csv_filename = "attendance_log.csv"
with open(csv_filename, mode='a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Gesture"])  # Write header only once

logged_gestures = set()  # To prevent repeated logging of same gesture in same frame

# === Gesture detection helpers ===
def is_close(point1, point2, threshold=0.1):
    distance = math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    return distance < threshold

def log_attendance(gesture):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, gesture])


def is_thumbs_up(landmarks):
    thumb_tip = landmarks[4]
    thumb_base = landmarks[2]

    if thumb_tip.y < thumb_base.y:
        other_fingers = [5, 9, 13, 17]  # Other finger landmarks (excluding thumb)
        for finger in other_fingers:
            if landmarks[finger].y < landmarks[finger - 2].y:
                return False
        return True  # All conditions for "thumbs up" are met
    return False


def get_gesture(landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    close_count = 0
    for i in tips[1:]:
        if is_close(landmarks[4], landmarks[i], threshold=0.1):
            close_count += 1

    if fingers == [1, 1, 1, 1, 1]:   # open palm
        return "Enter"
    elif is_thumbs_up(landmarks): # thumps up
        return "Break-In"
    elif fingers == [0, 0, 0, 0, 0]: # hand closed
        return "Leave"
    elif fingers[1:] == [0, 1, 1, 1] and is_close(landmarks[4], landmarks[8]): # super gesture
        return "Break-Out"


    return "None"

# === Main loop ===
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    gesture_text = "No Hand Gesture Detected"

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

            gesture = get_gesture(handLms.landmark)
            if gesture != "None":
                gesture_text = gesture

                # Log only if this gesture wasn't logged in the last few frames
                if gesture not in logged_gestures:
                    log_attendance(gesture)
                    logged_gestures = {gesture}  # Reset with new gesture

            else:
                logged_gestures.clear()  # Reset when hand disappears or gesture is None

    cv2.putText(frame, gesture_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 215, 0), 2)
    cv2.imshow("Attendance Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





