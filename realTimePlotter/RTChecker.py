import time

t = time.time()

while True:
    if time.time() - t > 1:
        print("Heyy")
        t = time.time()