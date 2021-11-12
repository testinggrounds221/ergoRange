import time
import os

now = time.localtime(time.time())
print("Session{}_{}_{}_{}_{}_{}".format(now.tm_year, now.tm_mon, now.tm_mday,
                                        now.tm_hour, now.tm_min, now.tm_sec))

print(os.getcwd())
parent_dir = os.getcwd()
path = os.path.join(parent_dir, "session")
os.mkdir(path)