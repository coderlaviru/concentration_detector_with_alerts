# Concentration Detector with Alerts

A real-time computer vision application that monitors a user's concentration level using facial landmarks, eye movement, gaze direction, head position, and blinking behavior.

The system uses a webcam to analyze facial features and generates a real-time concentration score. It also detects prolonged distraction, provides a visual alert, and stores concentration data in a CSV file for later analysis.

---

## Features

- Real-time concentration monitoring using a webcam
- Face landmark detection using MediaPipe Face Mesh
- Eye Aspect Ratio (EAR) based blink detection
- Gaze direction estimation
- Head position monitoring
- Real-time concentration score from 0–100%
- Concentration progress bar
- Distraction counter
- Automatic distraction alert
- Popup warning using Tkinter
- Concentration data logging in CSV format
- Facial landmark visualization
- Real-time OpenCV interface

---

## How It Works

The application analyzes facial landmarks captured through the webcam and evaluates three main visual indicators:

### 1. Gaze Detection

The system uses iris landmarks detected by MediaPipe to estimate the horizontal gaze position.

If the estimated gaze falls within the defined screen-facing range, the gaze component contributes positively to the concentration score.

### 2. Head Position Detection

The system uses the nose landmark to estimate whether the user's head is approximately centered relative to the camera.

If the head is within the defined position range, the head-position component contributes positively to the concentration score.

### 3. Blink Detection

The system calculates the Eye Aspect Ratio (EAR) using facial landmarks around both eyes.

A low EAR indicates that the eyes may be closed or blinking.

---

## Concentration Score

The concentration score is calculated using three components:

```text
Gaze       → 40%
Head Pose  → 40%
Blink      → 20%
````

The calculation is:

```text
Concentration Score =
(0.4 × Gaze)
+ (0.4 × Head Position)
+ (0.2 × Eye Status)
```

The final score is converted into a percentage between `0` and `100`.

Example:

```text
Concentration: 78%
```

---

## Distraction Detection

The application considers the user distracted when the concentration score falls below `40%`.

A distraction counter is then increased while the low concentration condition continues.

If the user remains distracted for more than 30 consecutive frames, the application displays a popup warning:

```text
Distraction Alert

You seem distracted! Please refocus.
```

Once the concentration improves, the distraction counter is reset.

---

## Score Smoothing

To reduce sudden fluctuations in the concentration score, the application stores the latest 10 scores using a deque.

```python
history = deque(maxlen=10)
```

The average of these recent scores is used as the displayed concentration score.

This helps make the displayed result more stable instead of changing significantly from frame to frame.

---

## Data Logging

The application automatically creates a CSV file:

```text
concentration_log.csv
```

The file contains:

| Timestamp     | Concentration Score | Distracted   |
| ------------- | ------------------- | ------------ |
| Date and Time | Score from 0–100    | True / False |

Example:

```text
Timestamp,Concentration Score,Distracted
2026-09-17 10:30:15,82,False
2026-09-17 10:30:16,79,False
2026-09-17 10:30:17,35,True
```

This allows the user's concentration activity to be recorded throughout the monitoring session.

---

## Technologies Used

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **Tkinter**
* **CSV**
* **Deque**
* **Time**

---

## Libraries Used

The project uses the following Python libraries:

```text
opencv-python
mediapipe
numpy
```

The following modules are also used from Python's standard library:

```text
collections
csv
time
tkinter
os
```

---

## Project Structure

```text
concentration_detector_with_alerts/
│
├── concentration_detector.py
├── concentration_log.csv
├── README.md
└── requirements.txt
```

### Files

**`concentration_detector.py`**

Contains the main application code for webcam capture, facial landmark detection, concentration calculation, distraction detection, alerts, and logging.

**`concentration_log.csv`**

Stores the concentration score and distraction status generated during execution.

**`README.md`**

Contains project documentation and usage instructions.

**`requirements.txt`**

Contains the Python dependencies required to run the project.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/coderlaviru/concentration_detector_with_alerts.git
```

Move into the project directory:

```bash
cd concentration_detector_with_alerts
```

---

### Step 2: Install Required Libraries

Install the required dependencies using:

```bash
pip install opencv-python mediapipe numpy
```

---

### Step 3: Run the Application

Run the Python file:

```bash
python concentration_detector.py
```

The webcam will start and the concentration monitoring window will appear.

---

## Usage

1. Connect or enable your webcam.
2. Run the Python application.
3. Allow camera access if requested.
4. Sit in front of the webcam.
5. Keep your face visible to the camera.
6. The system detects facial landmarks in real time.
7. Your concentration score is calculated continuously.
8. The score is displayed on the screen.
9. If concentration remains low, the distraction counter increases.
10. A popup alert appears after prolonged distraction.
11. Concentration data is automatically stored in the CSV log file.

---

## Exiting the Application

To stop the application, press:

```text
Q
```

while the OpenCV window is active.

The webcam will be released and the application will close.

---

## Main Components

### Face Mesh Detection

MediaPipe Face Mesh is used to detect facial landmarks.

```python
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True
)
```

The `refine_landmarks=True` option provides more detailed landmarks, including iris-related landmarks.

---

### Eye Aspect Ratio

The application uses six landmarks for each eye.

The Eye Aspect Ratio is calculated as:

```text
EAR = (A + B) / (2 × C)
```

where:

* `A` = vertical distance between two eye landmarks
* `B` = second vertical eye distance
* `C` = horizontal eye distance

A smaller EAR indicates that the eye is likely closed.

---

### Blink Detection

The system checks whether the calculated EAR is below the defined threshold.

```python
def is_blinking(ear, threshold=0.2):
    return ear < threshold
```

If the EAR is below the threshold, the system treats the current frame as a blinking/closed-eye frame.

---

### Gaze Score

The iris landmarks are used to estimate the user's gaze position.

The system calculates the average horizontal iris position and checks whether it falls inside a predefined range.

```python
def compute_gaze_score(landmarks):
    x = (landmarks[468].x + landmarks[473].x) / 2
    return 1.0 if 0.45 < x < 0.65 else 0.0
```

---

### Head Pose Score

The nose landmark is used to estimate whether the user's face is approximately centered.

```python
def compute_head_pose_score(landmarks, w, h):
    nose = landmarks[1]

    dx = abs(nose.x - 0.5) * w
    dy = abs(nose.y - 0.5) * h

    return 1.0 if dx < 0.2 * w and dy < 0.2 * h else 0.0
```

---

### Concentration Calculation

The final concentration score combines gaze, head position, and eye status.

```python
def concentration_score(gaze, head, blink):
    return round(
        (0.4 * gaze +
         0.4 * head +
         0.2 * (0 if blink else 1)) * 100,
        2
    )
```

---

### Concentration Bar

The application displays a visual concentration bar using OpenCV.

The bar changes according to the calculated concentration score.

Example:

```text
Concentration: 85%
█████████████████
```

A lower score results in a shorter concentration bar.

---

### Distraction Counter

When the smoothed concentration score is below `40`, the distraction counter increases.

```python
if smooth < 40:
    distraction_counter += 1
    distracted = True
```

When concentration improves, the counter is reset.

```python
else:
    distraction_counter = 0
```

---

### Alert System

When the distraction counter exceeds 30 frames, a Tkinter popup is displayed.

```python
show_popup()
```

The alert message is:

```text
You seem distracted! Please refocus.
```

---

## Output

The live monitoring window displays:

* Webcam feed
* Face landmarks
* Concentration score
* Concentration bar
* Distraction counter
* Visual facial tracking

Example:

```text
Concentration: 82%

Distracted: 0
```

If the user becomes distracted:

```text
Concentration: 35%

Distracted: 18
```

---

## Applications

This project can be used as a prototype for:

* Online learning
* Student study sessions
* Productivity monitoring
* Computer-based attention monitoring
* Human-computer interaction
* Computer vision experiments
* Webcam-based user monitoring

---

## Limitations

This project provides an estimated concentration score based on visual features. It does not directly measure a person's psychological or cognitive concentration.

Some limitations include:

* Webcam positioning can affect detection accuracy.
* Poor lighting can affect facial landmark detection.
* Camera quality can influence the results.
* Gaze estimation uses a predefined landmark range.
* Head pose estimation uses a simplified landmark-based approach.
* Individual differences in eye shape and facial structure may affect blink detection.
* The concentration threshold is predefined.
* The system is primarily designed for a single user.
* The system does not use a calibrated eye-tracking device.

---

## Future Improvements

Possible future improvements include:

* More accurate gaze estimation
* Camera calibration
* Advanced head-pose estimation
* Personalized concentration thresholds
* Session-wise concentration statistics
* Concentration graphs
* Daily and weekly reports
* Streamlit dashboard
* Improved alert customization
* Session summary generation
* Database-based storage
* Multi-user support
* Improved facial behavior analysis

---

## Learning Outcomes

Through this project, the following concepts were implemented:

* Computer Vision
* Facial Landmark Detection
* MediaPipe Face Mesh
* Eye Aspect Ratio
* Blink Detection
* Gaze Estimation
* Basic Head Pose Estimation
* Real-Time Video Processing
* OpenCV
* Data Logging
* GUI Integration
* Real-Time Monitoring

---

## Author

**Lakshita Sharma**

B.Tech CSE (AI & ML)

GitHub:
[https://github.com/coderlaviru](https://github.com/coderlaviru)

