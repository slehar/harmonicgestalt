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
#CHUNK     = 8192     # frames per buffer 
CHUNK     = 4410     # audio buffsize   
plotWidth = 500
twoPi = float(2.0*np.pi)

# Set time and data arrays    
time  = np.linspace(0, twoPi, num=CHUNK)     # time 
fData = np.zeros(CHUNK, dtype=float)     # data
for freq in [700, 800, 900]:
    fData += np.sin(time*freq/10.)
fData = fData / np.max(np.abs(fData))
iData = np.uint8(fData * 127. + 128.)
#lastTime = time[-1] + (time[-1] - time[-2])
lastTime = 0.

####### Open figure and set axes 1 for drawing Artists ########
plt.close('all')
fig = plt.figure(figsize=(12,8))
aspect = 10./8.
fig.canvas.set_window_title('Test Audio')

#### Axes 1 ####
ax1 = fig.add_axes([.05,.4,.4,.2])
ax1.set_xlim([0., plotWidth])
ax1.set_xticks(list(np.linspace(0, plotWidth, plotWidth/100)))
plt.grid(True)
ax1.set_ylim([-2,2])
ax1.set_yticks(np.linspace(-2,2,9))
ax1.set_title('Beginning of buffer')
plt.sca(ax1)
plotLines1 = ax1.plot(range(plotWidth), fData[:plotWidth])

#### Axes 2 ####
ax2 = fig.add_axes([.55,.4,.4,.2])
ax2.set_xlim([CHUNK-plotWidth, CHUNK])
#ax2.set_xticks(list(np.linspace(0, plotWidth, plotWidth/100)))
plt.grid(True)
#ax2.set_xlim([0, plotWidth])
ax2.set_ylim([-2,2])
ax2.set_yticks(np.linspace(-2,2,9))
ax2.set_title('End of buffer')
plt.sca(ax2)
plotLines2 = ax2.plot(range(CHUNK, CHUNK-plotWidth, -1), fData[CHUNK-plotWidth:CHUNK])

# PyAudio Callback - gets called repeatedly
def paCallback(in_data, frame_count, time_info, status):
    global iData
    return (iData, pyaudio.paContinue)

# PyAudio open audio stream
pa = pyaudio.PyAudio()
stream = pa.open(
            format = pa.get_format_from_width(1),
            channels = 1,
            rate = RATE,
            output = True,
            stream_callback=paCallback,
            frames_per_buffer=CHUNK)

# Keypress 'q' to quit
def press(event):
    global ptList, data
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
fig.canvas.mpl_connect('key_press_event', press)


#  frequency slider
axSlider1 = fig.add_axes([0.3, 0.125, 0.234, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])
slider1 = Slider(axSlider1, 'frequency', 100, 1000.,
                 valinit=700., valfmt='%0.0f')
freq = slider1.val/10.

def update1(val):
    global freq, iData, fData, time
    freq = slider1.val/10.
    iFreq = freq / 10.
    fData = np.zeros(CHUNK, dtype=float)
    fData += np.sin(time*freq)
    fData = fData / np.max(np.abs(fData))

    plotLines1[0].set_ydata(fData[:plotWidth])
    plotLines2[0].set_ydata(fData[CHUNK-plotWidth:CHUNK])
    iData = np.uint8(fData * 127 + 128)
    plt.pause(.001)
    
slider1.on_changed(update1)


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


