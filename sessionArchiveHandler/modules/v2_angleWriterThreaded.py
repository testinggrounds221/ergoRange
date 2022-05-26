import cv2
import mediapipe as mp
import numpy as np
import csv
import time
import threading

LINE_WIDTH = 2
KNEE_RANGE = (120, 80)
ELBOW_RANGE = (120, 80)
SPINE_RANGE = (120, 80)
FIELD_NAMES = ["Time", "Elbow", "Knee", "Spine"]
T = time.time()
x = 0
p1 = 0
p2 = 0
p3 = 0
angle1 = 0
angle2 = 0
angle3 = 0

# Elbow, Knee, Spine
mp_pose = mp.solutions.pose

# cap = cv2.VideoCapture("s.mp4")
cap = cv2.VideoCapture(0)


def writeAccuracy(accuracyDict, session):
    with open(session + '/accuracy.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        # print(accuracyDict)
        csv_writer.writerow(accuracyDict)


def writeAngle(angleDict, session):
    with open(session + '/angle.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        # print(angleDict)
        csv_writer.writerow(angleDict)


def getDescription(jointNo, input, angleRange):
    # Elbow, Knee, Spine
    pos = 0
    if input > angleRange[0]: pos = 2
    elif input < angleRange[1]: pos = 1
    if (jointNo == 0 and pos == 0): return "Elbow Position is Correct"
    if (jointNo == 0 and pos == 1): return "Elbow Position is Acute"
    if (jointNo == 0 and pos == 2): return "Elbow Position is Obtuse"

    if (jointNo == 1 and pos == 0): return "Knee Position is Correct"
    if (jointNo == 1 and pos == 1): return "Knee Position is Acute"
    if (jointNo == 1 and pos == 2): return "Knee Position is Obtuse"

    if (jointNo == 2 and pos == 0): return "Spine Position is Correct"
    if (jointNo == 2 and pos == 1): return "Spine Position is Acute"
    if (jointNo == 2 and pos == 2): return "Spine Position is Obtuse"


def getPercentageFromAngle(input, angleRange):
    if input > angleRange[0] or input < angleRange[1]: return 0
    return ((abs(input - angleRange[1])) * 100) / abs(angleRange[0] -
                                                      angleRange[1])
    # return (round((abs(input - angleRange[1])) * 100) /
    #         abs(angleRange[0] - angleRange[1]), 2)


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


def writeData(session):
    global x, p1, p2, p3, angle1, angle2, angle3

    while (True):
        try:
            time.sleep(1)
            x = x + 1
            writeAccuracy(
                {
                    FIELD_NAMES[0]: x,
                    FIELD_NAMES[1]: p1,
                    FIELD_NAMES[2]: p2,
                    FIELD_NAMES[3]: p3
                }, session)

            writeAngle(
                {
                    FIELD_NAMES[0]: x,
                    FIELD_NAMES[1]: angle1,
                    FIELD_NAMES[2]: angle2,
                    FIELD_NAMES[3]: angle3
                }, session)
        except KeyboardInterrupt:
            break


def detectPose():
    global x, p1, p2, p3, angle1, angle2, angle3

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

                pointG = [landmarks[11].x, landmarks[11].y]  # Spine
                pointH = [landmarks[23].x, landmarks[23].y]
                pointI = [landmarks[25].x, landmarks[25].y]

                # Calculate angle
                angle1 = calculate_angle(pointA, pointB, pointC)
                angle2 = calculate_angle(pointD, pointE, pointF)
                angle3 = calculate_angle(pointG, pointH, pointI)

                # Visualize angle
                cv2.putText(image, getDescription(0, angle1, KNEE_RANGE),
                            tuple(np.multiply(pointB, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                            cv2.LINE_AA)

                cv2.putText(image, getDescription(1, angle1, ELBOW_RANGE),
                            tuple(np.multiply(pointB, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                            cv2.LINE_4)

                cv2.putText(image, getDescription(3, angle3, SPINE_RANGE),
                            tuple(np.multiply(pointH, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1,
                            cv2.LINE_AA)

                p1 = getPercentageFromAngle(angle1, ELBOW_RANGE)
                color1 = getClrFromPercentage(p1)
                image = cv2.line(
                    image, tuple(np.multiply(pointA, [640, 480]).astype(int)),
                    tuple(np.multiply(pointB, [640, 480]).astype(int)), color1,
                    LINE_WIDTH)
                image = cv2.line(
                    image, tuple(np.multiply(pointB, [640, 480]).astype(int)),
                    tuple(np.multiply(pointC, [640, 480]).astype(int)), color1,
                    LINE_WIDTH)

                p2 = getPercentageFromAngle(angle2, KNEE_RANGE)
                color2 = getClrFromPercentage(p2)
                image = cv2.line(
                    image, tuple(np.multiply(pointD, [640, 480]).astype(int)),
                    tuple(np.multiply(pointE, [640, 480]).astype(int)), color2,
                    LINE_WIDTH)
                image = cv2.line(
                    image, tuple(np.multiply(pointE, [640, 480]).astype(int)),
                    tuple(np.multiply(pointF, [640, 480]).astype(int)), color2,
                    LINE_WIDTH)

                p3 = getPercentageFromAngle(angle3, SPINE_RANGE)
                color3 = getClrFromPercentage(p3)
                image = cv2.line(
                    image, tuple(np.multiply(pointG, [640, 480]).astype(int)),
                    tuple(np.multiply(pointH, [640, 480]).astype(int)), color2,
                    LINE_WIDTH)
                image = cv2.line(
                    image, tuple(np.multiply(pointH, [640, 480]).astype(int)),
                    tuple(np.multiply(pointI, [640, 480]).astype(int)), color2,
                    LINE_WIDTH)
                # print(angle1, angle2, angle3)
            except Exception as e:
                print(e)
                pass
            image = cv2.resize(image, (960, 540))
            cv2.imshow('Ergonomic Check', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def start(session):
    global x, p1, p2, p3, angle1, angle2, angle3

    with open(session + '/accuracy.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()

    with open(session + '/angle.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()

    writeDataThread = threading.Thread(target=writeData, args=(session, ))
    writeDataThread.start()

    detectPoseThread = threading.Thread(target=detectPose)
    detectPoseThread.start()


if __name__ == "__main__":
    start("Sample")
