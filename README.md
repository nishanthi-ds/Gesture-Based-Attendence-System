# 🖐️ Hand Gesture-Based Attendance System

This Python project uses **MediaPipe** and **OpenCV** to recognize specific hand gestures via webcam and logs attendance activities like **Enter**, **Leave**, **Break-In**, and **Break-Out** into a CSV file.

---

## 📌 Features

* Real-time hand gesture detection via webcam.
* Recognizes 4 unique gestures:
  * ✋ **Enter** – All fingers up.
  * ✊ **Leave** – All fingers down.
  * 🤙 **Break-In** –thumbs up
  * 👌 **Break-Out** – thumb close to index., other fingers up 
* Logs gesture name and timestamp in `attendance_log.csv`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nishanthi-ds/Gesture-Based-Attendence-System.git
cd Attendence_gesture
```

### Step 2: Install Dependencies

Make sure Python 3.7+ is installed, then run the following command to install the necessary libraries:

```bash
pip install opencv-python mediapipe
```

### Step 3: Run the Application
Save the Python script as `attendance.py` and run it with the following command:

```bash
python attendance.py
```

This will open your webcam, and the system will start recognizing hand gestures. The gestures will be logged along with the timestamp in a CSV file named `attendance_log.csv`.

### Step 4: Define Gestures
Here are the gestures recognized by the system:

| Gesture Name | Finger Positions                               | Description                                    |
|--------------|------------------------------------------------|------------------------------------------------|
| Enter        | All fingers up                                 | Marks the start of attendance.                 |
| Leave        | All fingers down                               | Marks the end of attendance.                   |
| Break-In     | All fingers up, thumb close to at least 3 fingers | Marks the start of a break.                    |
| Break-Out    | Index finger up, other fingers down, thumb close to index | Marks the end of a break.         |

### Step 5: Quit the Webcam Feed
To quit the webcam feed, press the **'q'** key.

## CSV Log Format
The system logs the gestures along with timestamps in the following format:

```csv
Timestamp,Gesture
2025-04-17 10:00:00,Enter
2025-04-17 10:05:00,Leave
```

