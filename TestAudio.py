# -*- coding: utf-8 -*-
"""
TestAudio.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
import numpy as np
import pyaudio

# global variables
RATE      = 44100    # bytes per second data rate
BASEFREQ  = 500      # base frequency Hz
CHUNK     = 8192     # frames per buffer 
plotWidth = 512
twoPi = float(2.0*np.pi)
data  = np.zeros(RATE, dtype=float)     # buffer of data
time  = np.linspace(0, twoPi, RATE)     # time of data
fData = np.sin(time)
freq = 0.

    
# PyAudio Callback - gets called repeatedly
def paCallback(in_data, frame_count, time_info, status):
    global data
    plotLines1[0].set_ydata(data[:plotWidth])
    plotLines2[0].set_ydata(data[RATE-plotWidth:RATE])
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
fig = plt.figure(figsize=(12,8))
aspect = 10./8.
fig.canvas.set_window_title('Test Audio')

#### Axes 1 ####
ax1 = fig.add_axes([.05,.4,.4,.2])
ax1.set_xlim([0., plotWidth])
ax1.set_ylim([0,255])
plt.sca(ax1)
plotLines1 = plt.plot(data[:plotWidth])

#### Axes 2 ####
ax2 = fig.add_axes([.55,.4,.4,.2])
#ax2.set_xlim([RATE-plotWidth, RATE])
ax2.set_xlim([0, plotWidth])
ax2.set_ylim([0,255])
plt.sca(ax2)
plotLines2 = plt.plot(data[RATE-plotWidth:RATE])


# Keypress 'q' to quit
def press(event):
    global ptList, data
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
fig.canvas.mpl_connect('key_press_event', press)

#plt.ion()

#  frequency slider
#axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
#axSlider1.set_xticks([])
#axSlider1.set_yticks([])
#slider1 = Slider(axSlider1, 'frequency', 100, 1000., valinit=300.)
#freq = slider1.val
#
#def update1(val):
#    global freq, data, fData, time
#    freq = slider1.val
#    fData = np.zeros(RATE, dtype=float)
#    fData += np.sin(time*freq)
#    fData = fData / np.max(np.abs(fData)) * 127 + 128
#    lastTime = time[-1] + (time[-1] - time[-2])
#    time = np.linspace(lastTime, lastTime+twoPi, RATE)
#    plt.sca(ax)
#    data = np.uint8(fData)
#    plt.pause(.001)
#    
#slider1.on_changed(update1)


# start the stream (4)
#stream.start_stream()

# Show plot
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)


