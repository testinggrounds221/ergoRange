import pandas as pd
import time
from os import system
import winsound
import threading


def printStatus(session, pointer):
    print(pointer)
    df = pd.read_csv(session + '/angle.csv')
    data = df.iloc[pointer - 5:pointer, :]
    elbowMean = data['Elbow'].mean()
    kneeMean = data['Knee'].mean()
    spineMean = data['Spine'].mean()

    # IF MEANS ARE NOT IN RANGE, PRINT ERROR MSG AND PLAY SOUND HERE
    # winsound.Beep(500, 1000)
    print("elbowMean ", elbowMean)
    print("kneeMean ", kneeMean)
    print("spineMean ", spineMean)


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
