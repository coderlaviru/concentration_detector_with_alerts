# concentration_detector_with_alerts
AI-Based Concentration Tracker

A real-time concentration monitoring system powered by AI, designed to detect and track focus levels using facial landmarks.
This project uses MediaPipe, OpenCV, and Tkinter to assess attention based on eye movement, head posture, and blink detection.

Features:

- Real-time Concentration Detection
- Eye Aspect Ratio for blink detection
- Head Pose Estimation
- Gaze Estimation using iris tracking
- Smooth concentration bar with distraction counter
- Popup alert using GUI if user is distracted
- Automatic logging to CSV for personal analytics

Demo:
in the mp4 file

Requirements:

- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- Tkinter (standard with Python)

install manually:
pip install opencv-python mediapipe numpy

CSV Logging:

- All session scores and distraction status are saved in concentration_log.csv
- Format: Timestamp, Concentration Score, Distracted

Tools & Libraries Used:

- OpenCV
- MediaPipe
- NumPy
- Tkinter

To-Do / Future Plans:

- Add sound alerts alongside popups
- Multi-user support
- Dashboard analytics
- Break timer integration
- .exe packaging with autostart

Contributing:
Pull requests, ideas, and suggestions are welcome!

License:
This project is licensed under the MIT License. See the LICENSE file for details.
