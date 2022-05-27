import pandas as pd
import time
from os import system
import winsound
import threading
import screen_brightness_control as sbc
# set flags for user config
initBrightness = sbc.get_brightness()[0]
isPlaySound = True
isDimScreen = True


def notifyUser():
    print("Notifying User...")
    if isPlaySound:
        winsound.Beep(500, 5000)
    if isDimScreen: sbc.set_brightness(initBrightness - 20)


def normalConfig():
    if isDimScreen: sbc.set_brightness(initBrightness)


def printStatus(session, pointer):
    # print(pointer)
    df = pd.read_csv(session + '/angle.csv')
    data = df.iloc[pointer - 5:pointer, :]
    elbowMean = data['Elbow'].mean()
    kneeMean = data['Knee'].mean()
    spineMean = data['Spine'].mean()

    # IF MEANS ARE NOT IN RANGE, PRINT ERROR MSG AND PLAY SOUND HERE
    # winsound.Beep(500, 1000)

    if (elbowMean < 50):
        print("Elbows are too Constricted. May lead to Muscular Cramps")
        notifyUser()
    else:
        normalConfig()

    if (spineMean < 50):
        print("Spine region is too bent. May lead to Hunching")
    #     notifyUser()
    # else:
    #     normalConfig()
    if (spineMean > 130):
        print("Spine region is in bad posture. May lead to chronic back pain")
    #     notifyUser()
    # else:
    #     normalConfig()

    if (kneeMean < 50):
        print(
            "Knee region is consrtricted. May lead to uneven Pressure Distribution"
        )
    #     notifyUser()
    # else:
    #     normalConfig()
    if (kneeMean > 130):
        print("Knee region is in bad posture. May lead to knee pain")
    #     notifyUser()
    # else:
    #     normalConfig()


def output(session):
    time.sleep(2)
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
