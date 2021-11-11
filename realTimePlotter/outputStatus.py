import pandas as pd
import time
from os import system
import winsound
import threading


def printStatus(pointer):
    print(pointer)
    df = pd.read_csv('angle.csv')
    data = df.iloc[pointer - 5:pointer, :]
    elbowMean = data['Elbow'].mean()
    kneeMean = data['Knee'].mean()
    spineMean = data['Spine'].mean()

    # IF MEANS ARE NOT IN RANGE, PRINT ERROR MSG AND PLAY SOUND HERE
    # winsound.Beep(500, 1000)
    print("elbowMean ", elbowMean)
    print("kneeMean ", kneeMean)
    print("spineMean ", spineMean)


def output():
    time.sleep(5)
    pointer = 5
    while (True):
        printStatus(pointer)
        pointer = pointer + 5
        time.sleep(5)
        system('cls')


def start():
    outputThread = threading.Thread(target=output)
    outputThread.start()


if __name__ == "__main__":
    start()
