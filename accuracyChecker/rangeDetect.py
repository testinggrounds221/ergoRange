import cv2
import mediapipe as mp
import numpy as np

LINE_WIDTH = 2
mp_pose = mp.solutions.pose


def getPercentageFromAngle(input, max, min):
    if input > max or input < min: return 0
    return ((abs(input - min)) * 100) / abs(max - min)


def getClrFromPercentage(percentage):
    if percentage > 50:
        red = 1 - 2 * (percentage - 50) / 100.0
    else:
        red = 1.0

    if percentage > 50:
        green = 1.0
    else:
        green = 2 * percentage / 100.0
    blue = 0.0
    return ((int)(blue * 255), (int)(green * 255), (int)(red * 255))


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

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            pointA = [landmarks[11].x, landmarks[11].y]  # Elbow
            pointB = [landmarks[13].x, landmarks[13].y]
            pointC = [landmarks[15].x, landmarks[15].y]

            pointD = [landmarks[23].x, landmarks[23].y]  # Knee
            pointE = [landmarks[25].x, landmarks[25].y]
            pointF = [landmarks[27].x, landmarks[27].y]

            pointG = [landmarks[11].x, landmarks[11].y]  # Knee
            pointH = [landmarks[23].x, landmarks[23].y]
            pointI = [landmarks[25].x, landmarks[25].y]

            # Calculate angle
            angle1 = calculate_angle(pointA, pointB, pointC)
            angle2 = calculate_angle(pointD, pointE, pointF)
            angle3 = calculate_angle(pointG, pointH, pointI)

            # Visualize angle
            cv2.putText(image, str(angle1),
                        tuple(np.multiply(pointB, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(image, str(angle2),
                        tuple(np.multiply(pointB, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(image, str(angle3),
                        tuple(np.multiply(pointH, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
                        cv2.LINE_AA)
            color1 = getClrFromPercentage(
                getPercentageFromAngle(angle1, 120, 80))
            image = cv2.line(
                image, tuple(np.multiply(pointA, [640, 480]).astype(int)),
                tuple(np.multiply(pointB, [640, 480]).astype(int)), color1,
                LINE_WIDTH)

            image = cv2.line(
                image, tuple(np.multiply(pointB, [640, 480]).astype(int)),
                tuple(np.multiply(pointC, [640, 480]).astype(int)), color1,
                LINE_WIDTH)

            color2 = getClrFromPercentage(
                getPercentageFromAngle(angle2, 120, 80))
            image = cv2.line(
                image, tuple(np.multiply(pointD, [640, 480]).astype(int)),
                tuple(np.multiply(pointE, [640, 480]).astype(int)), color2,
                LINE_WIDTH)

            image = cv2.line(
                image, tuple(np.multiply(pointE, [640, 480]).astype(int)),
                tuple(np.multiply(pointF, [640, 480]).astype(int)), color2,
                LINE_WIDTH)

            color3 = getClrFromPercentage(
                getPercentageFromAngle(angle3, 120, 80))
            image = cv2.line(
                image, tuple(np.multiply(pointG, [640, 480]).astype(int)),
                tuple(np.multiply(pointH, [640, 480]).astype(int)), color2,
                LINE_WIDTH)

            image = cv2.line(
                image, tuple(np.multiply(pointH, [640, 480]).astype(int)),
                tuple(np.multiply(pointI, [640, 480]).astype(int)), color2,
                LINE_WIDTH)

        except:
            print("CAMERA ERROR")
            pass

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
