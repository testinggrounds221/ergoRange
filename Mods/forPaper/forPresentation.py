import cv2
import mediapipe as mp
import numpy as np

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


cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
stage = None
isCorrect = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

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
            pointA = [landmarks[10].x, landmarks[10].y]
            pointB = [landmarks[12].x, landmarks[12].y]
            pointC = [landmarks[24].x, landmarks[24].y]

            pointD = [landmarks[9].x, landmarks[9].y]
            pointE = [landmarks[11].x, landmarks[11].y]
            pointF = [landmarks[23].x, landmarks[23].y]
            # Calculate angle
            angle1 = calculate_angle(pointA, pointB, pointC)
            angle2 = calculate_angle(pointD, pointE, pointF)

            # Visualize angle
            cv2.putText(image, str(angle1),
                        tuple(np.multiply(pointB, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(image, str(angle2),
                        tuple(np.multiply(pointE, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2,
                        cv2.LINE_AA)

            # Curl counter logic
            # if angle1 > 90 and angle2 > 90 and angle1 < 130 and angle2 < 130:
            #     # stage = "Elbows are in right Position"
            #     stage = "Knees are in Right Position"
            #     isCorrect = True
            # if angle1 < 90 or angle2 < 90:
            #     stage = "Knees are Bent too much"
            #     isCorrect = False

            # if angle1 > 110 or angle2 > 110:
            #     stage = "Knees are Stretched too much"
            #     isCorrect = False

            if angle1 >= 140 and angle1 <= 150:
                # stage = "Elbows are in right Position"
                stage = "Upper back is in Right Position"
                isCorrect = True
            elif angle1 < 140:
                stage = "Upper back is Slouched too much"
                isCorrect = False
            elif angle1 > 150:
                stage = "Upper back is Stretched too much"
                isCorrect = False

        except:
            pass

        # Render curl counter
        # Setup status box
        # cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

        # Rep data

        # Stage data
        # cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #             (0, 0, 0), 1, cv2.LINE_AA)
        color = ((0, 0, 255), (255, 0, 0))[bool(isCorrect)]

        cv2.putText(image, stage, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                    1, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66),
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230),
                                   thickness=2,
                                   circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
