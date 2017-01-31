# -*- coding: utf-8 -*-
"""
TestAudio.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pyaudio

# global variables
ptRad     = .01      # Radius of points
RATE      = 44100    # bytes per second data rate
BASEFREQ  = 500      # base frequency Hz
CHUNK     = 8192     # frames per buffer 
PLOTWIDTH = 512      # Width of plot trace
twoPi = float(2.0*np.pi)
data  = np.zeros(RATE, dtype=float)     # buffer of data
time  = np.linspace(0, twoPi, RATE)     # time of data
fData = np.sin(time)
#plotTime = np.linspace(0, twoPi, num=PLOTWIDTH)
plotTime = np.arange(0, twoPi, twoPi/PLOTWIDTH)
plotData = np.sin(plotTime) * 128 + 127

ptList = []
ptList.append({'xPos':.5, 'yPos':.5, 'selected':False})
selectedPt = None
freqList = []

buttonState = False
xdata, ydata = .5, .5

    
# PyAudio Callback - gets called repeatedly
def paCallback(in_data, frame_count, time_info, status):
    global data
    return (data, pyaudio.paContinue)

# PyAudio open audio stream
pa = pyaudio.PyAudio()
stream = pa.open(
            format = pa.get_format_from_width(1),
            channels = 1,
            rate = RATE,
            output = True,
            stream_callback=paCallback,
            frames_per_buffer=CHUNK)


fData = np.zeros(RATE, dtype=float)
for freq in [300, 400, 500]:
    fData += np.sin(time*freq)
fData = fData / np.max(np.abs(fData)) * 127 + 128
lastTime = time[-1] + (time[-1] - time[-2])
time = np.linspace(lastTime, lastTime+twoPi, RATE)
data = np.uint8(fData)


####### Open figure and set axes 1 for drawing Artists ########
plt.close('all')
fig = plt.figure(figsize=(10,8))
aspect = 10./8.
fig.canvas.set_window_title('Test Audio')

#### Main axes ####
ax = fig.add_axes([.1, .225, .7, .75])
ax.set_xlim([0., RATE])
ax.set_ylim([-1, 1])
#ax.set_xticks([])
#ax.set_yticks([])

# Keypress 'q' to quit
def press(event):
    global ptList, data
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
fig.canvas.mpl_connect('key_press_event', press)

# start the stream (4)
stream.start_stream()

plt.plot(data)

# Show plot
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)

