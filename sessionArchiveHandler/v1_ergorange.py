import modules.v2_angleWriterThreaded as aw
import modules.outputStatus as op
import modules.plotter as pt
import time
import os

now = time.localtime(time.time())

session = "sessions/Session{}_{}_{}_{}_{}_{}".format(now.tm_year, now.tm_mon,
                                                     now.tm_mday, now.tm_hour,
                                                     now.tm_min, now.tm_sec)

parent_dir = os.getcwd()
path = os.path.join(parent_dir, session)
os.mkdir(path)

aw.start(session)
op.start(session)
pt.start(session)