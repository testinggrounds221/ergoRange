import pandas as pd
import time
from os import system
import winsound

time.sleep(5)
pointer = 5


def printStatus(pointer):
    print(pointer)
    df = pd.read_csv('data.csv')
    data = df.iloc[pointer - 5:pointer, :]
    elbowMean = data['Elbow'].mean()
    kneeMean = data['Knee'].mean()
    spineMean = data['Spine'].mean()

    # IF MEANS ARE NOT IN RANGE, PRINT ERROR MSG AND PLAY SOUND HERE
    # winsound.Beep(500, 1000)
    print("elbowMean ", elbowMean)
    print("kneeMean ", kneeMean)
    print("spineMean ", spineMean)


while (True):
    printStatus(pointer)
    pointer = pointer + 5
    time.sleep(5)
    system('cls')
