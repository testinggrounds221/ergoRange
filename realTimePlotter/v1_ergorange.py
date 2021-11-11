from matplotlib.pyplot import plot
import v2_angleWriterThreaded
import outputStatus
import plotter

v2_angleWriterThreaded.start()
outputStatus.start()
plotter.start()