# 🏃‍♂️ Real-time Fall Detection System

## 📌 Project Overview
This project is a real-time Computer Vision system designed to detect human falls using a standard web camera. It is built as part of an engineering project, utilizing **MediaPipe** for 3D pose estimation and **OpenCV** for image processing and geometric calculations.

Unlike basic bounding-box methods, this system uses a Mechatronics/Systems approach, calculating trigonometric body angles and applying temporal validation to eliminate false positives.

## ⚙️ How it Works (Logic & Algorithms)
The detection mechanism relies on 3 core pillars:
1. **Vertical Distance Analysis:** Continuously monitors the Y-axis distance between the Head (Nose) and the Center of the Hips. A sudden drop indicates a potential fall.
2. **Torso Angle Calculation:** Uses the `atan2` trigonometric function to calculate the angle of the spine (from Shoulders to Hips) relative to the ground. An angle < 30° triggers a warning.
3. **Temporal Validation (Debouncing):** To prevent false alarms from quick actions like picking up items, the system features a `pose_tracker` (debounce counter). The "fall" state must be continuously maintained for **2 seconds (60 frames)** before triggering the final Red Alert.

## 🛠️ Technologies Used
* **Python 3**
* **OpenCV (`cv2`):** For hardware interfacing, frame manipulation, and UI drawing.
* **MediaPipe (`mp.solutions.pose`):** Google's AI framework for real-time human pose landmark tracking.

## 🚀 Installation & Running
Follow these steps to run the project on your local machine:

**1. Clone the repository**
```bash
git clone https://github.com/quangcody/vgu-fall-detection-alphatest.git
cd vgu-fall-detection-alphatest
