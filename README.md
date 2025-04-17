# 🖐️ Hand Gesture-Based Attendance System

This Python project uses **MediaPipe** and **OpenCV** to recognize specific hand gestures via webcam and logs attendance activities like **Enter**, **Leave**, **Break-In**, and **Break-Out** into a CSV file.

---

## 📌 Features

* Real-time hand gesture detection via webcam.
* Recognizes 4 unique gestures:
  * ✋ **Enter** – All fingers up.
  * ✊ **Leave** – All fingers down.
  * 🤙 **Break-In** – All fingers up & thumb close to at least 3 fingers.
  * 👆 **Break-Out** – Index finger up, other fingers down, thumb close to index.
* Logs gesture name and timestamp in `attendance_log.csv`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hand-gesture-attendance.git
cd hand-gesture-attendance
