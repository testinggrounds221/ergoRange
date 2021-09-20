import cv2
import mediapipe as mp
import numpy as np
import csv

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return round(angle, 3)


# cap = cv2.VideoCapture(1)

# Curl counter variables
counter = 0
stage = None
isCorrect = None

## Setup mediapipe instance
for i in range(1, 19):
    with open('eggs.csv', 'a', newline='') as csvfile:
        angleWriter = csv.writer(csvfile, delimiter=',')
        with mp_pose.Pose(min_detection_confidence=0.5,
                          min_tracking_confidence=0.5) as pose:

            frame = cv2.imread(f"{i}.jpg")
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinate s
                pointA = [landmarks[11].x, landmarks[11].y]
                pointB = [landmarks[23].x, landmarks[23].y]
                pointC = [landmarks[25].x, landmarks[25].y]

                pointD = [landmarks[9].x, landmarks[9].y]
                pointE = [landmarks[11].x, landmarks[11].y]
                pointF = [landmarks[23].x, landmarks[23].y]
                # Calculate angle
                angle1 = calculate_angle(pointA, pointB, pointC)
                angle2 = calculate_angle(pointD, pointE, pointF)
                angleWriter.writerow([i, angle1, angle2])
                print(f"{i}.jpg => {angle1} {angle2}")

            except:
                pass
