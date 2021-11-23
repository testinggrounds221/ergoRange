import pandas as pd
import time
from os import system
import winsound
import threading


def printStatus(session, pointer):
    # print(pointer)
    df = pd.read_csv(session + '/angle.csv')
    data = df.iloc[pointer - 5:pointer, :]
    elbowMean = data['Elbow'].mean()
    kneeMean = data['Knee'].mean()
    spineMean = data['Spine'].mean()

    # IF MEANS ARE NOT IN RANGE, PRINT ERROR MSG AND PLAY SOUND HERE
    # winsound.Beep(500, 1000)

    if (elbowMean < 75):
        print("Elbows are too Constricted. May lead to Muscular Cramps")

    if (spineMean < 75):
        print("Spine region is too bent. May lead to Hunching")
    if (spineMean > 130):
        print("Spine region is in bad posture. May lead to chronic back pain")

    if (kneeMean < 75):
        print(
            "Knee region is consrtricted. May lead to uneven Pressure Distribution"
        )
    if (kneeMean > 130):
        print("Knee region is in bad posture. May lead to knee pain")


def output(session):
    time.sleep(5)
    pointer = 5
    while (True):
        printStatus(session, pointer)
        pointer = pointer + 5
        time.sleep(5)
        system('cls')


def start(session):
    outputThread = threading.Thread(target=output, args=(session, ))
    outputThread.start()


if __name__ == "__main__":
    start("Sample")
