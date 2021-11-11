import time, threading

# t = time.time()

# while True:
#     if time.time() - t > 1:
#         print("Heyy")
#         t = time.time()


def writeData():
    while (True):
        time.sleep(2)
        print("Heyy")


thread = threading.Thread(target=writeData)
thread.start()