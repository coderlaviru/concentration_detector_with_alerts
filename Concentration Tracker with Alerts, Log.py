# Concentration Tracker with Alerts, Logging, and GUI Enhancements
# Author: Your Name

import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import csv
import time
import tkinter as tk
from tkinter import messagebox
import os

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# CSV Logger Setup
LOG_FILE = "concentration_log.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Concentration Score", "Distracted"])

def log_score(score, distracted):
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), score, distracted])

def get_eye_aspect_ratio(landmarks, indices, w, h):
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]
    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
    ear = (A + B) / (2.0 * C)
    return ear

def is_blinking(ear, threshold=0.2):
    return ear < threshold

def compute_gaze_score(landmarks):
    x = (landmarks[468].x + landmarks[473].x) / 2
    return 1.0 if 0.45 < x < 0.65 else 0.0

def compute_head_pose_score(landmarks, w, h):
    nose = landmarks[1]
    dx = abs(nose.x - 0.5) * w
    dy = abs(nose.y - 0.5) * h
    return 1.0 if dx < 0.2 * w and dy < 0.2 * h else 0.0

def concentration_score(gaze, head, blink):
    return round((0.4 * gaze + 0.4 * head + 0.2 * (0 if blink else 1)) * 100, 2)

def draw_concentration_bar(frame, score):
    width = 200
    fill = int(score * width / 100)
    cv2.rectangle(frame, (30, 30), (30 + width, 60), (50, 50, 50), -1)
    color = (0, 255, 0) if score > 50 else (0, 100, 255)
    cv2.rectangle(frame, (30, 30), (30 + fill, 60), color, -1)
    cv2.putText(frame, f"Concentration: {score}%", (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def show_popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Distraction Alert", "You seem distracted! Please refocus.")
    root.destroy()

def main():
    cap = cv2.VideoCapture(0)
    history = deque(maxlen=10)
    distraction_counter = 0
    alert_shown = False

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w, _ = frame.shape

        distracted = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                lm = face_landmarks.landmark

                left_ear = get_eye_aspect_ratio(lm, LEFT_EYE, w, h)
                right_ear = get_eye_aspect_ratio(lm, RIGHT_EYE, w, h)
                blink = is_blinking((left_ear + right_ear) / 2)

                gaze = compute_gaze_score(lm)
                head = compute_head_pose_score(lm, w, h)
                score = concentration_score(gaze, head, blink)

                history.append(score)
                smooth = int(np.mean(history))
                draw_concentration_bar(frame, smooth)

                if smooth < 40:
                    distraction_counter += 1
                    distracted = True
                    cv2.putText(frame, f"Distracted: {distraction_counter}", (30, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    distraction_counter = 0
                    alert_shown = False

                if distraction_counter > 30 and not alert_shown:
                    show_popup()
                    alert_shown = True

                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1)
                )

                log_score(smooth, distracted)

        cv2.imshow("Focus Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
