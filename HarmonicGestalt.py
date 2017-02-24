# -*- coding: utf-8 -*-
"""
HarmonicGestalt.py

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
CHUNK     = 4410     # frames per buffer 
PLOTWIDTH = 512      # Width of plot trace
twoPi = float(2.0*np.pi)
data  = np.zeros(CHUNK, dtype=float)     # buffer of data
time  = np.linspace(0, twoPi, CHUNK)     # time of data
fData = np.sin(time)
#plotTime = np.linspace(0, twoPi, num=PLOTWIDTH)
plotTime = np.arange(0, twoPi, twoPi/PLOTWIDTH)
#plotData = np.sin(plotTime) * 128 + 127
plotData = np.zeros_like(plotTime)

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

######## Keyboard callback updatewave ########

# Update Wave to be played based on current dot positions
def updateWave():
    global data, fData, time, ptList, freqList, line

    freqList = []
    if len(ptList) < 2:
        fData = np.zeros(CHUNK, dtype=float)
        data = np.uint8(fData)
        return
    elif len(ptList) == 2:
        dist = np.sqrt((ptList[0]['xPos'] - ptList[1]['xPos'])**2. +
                       (ptList[0]['yPos'] - ptList[1]['yPos'])**2.)
        freqList.append(int(BASEFREQ/dist))
    else:
        for point1 in ptList:
            for point2 in ptList:
                if point1 is not point2:
                    dist = np.sqrt((point1['xPos'] - point2['xPos'])**2. +
                                   (point1['yPos'] - point2['yPos'])**2.)
                    freqList.append(int(BASEFREQ/dist))
                                        
    fData = np.zeros(CHUNK, dtype=float)
    for freq in freqList:
        iFreq = float(int(freq/10.))
        fData += np.sin(time*iFreq)
    fData = fData / np.max(np.abs(fData)) * 127 + 128
    yData = np.abs(np.fft.fft(fData[:PLOTWIDTH]))
    yData /= 100.
#    yData /= yData.max()
#    yData = np.log(yData)
    yDataSwap = np.fft.fftshift(yData)
    line.set_ydata(yDataSwap)
    fig.canvas.draw()
    data = np.uint8(fData)


####### Open figure and set axes 1 for drawing Artists ########
plt.close('all')
fig = plt.figure(figsize=(10,8))
aspect = 10./8.
fig.canvas.set_window_title('Harmonic Gestalt')

#### Main axes ####
ax = fig.add_axes([.1, .225, .7, .75])
ax.set_xticks([])
ax.set_yticks([])

#### Axes for spectrum ####
axSpect = fig.add_axes([.1, .05, .7, .15])
axSpect.set_xlim([-3., 3.])
#axSpect.set_xticks([-500, 0, 500])
#axSpect.set_ylim([0., 255.])
axSpect.set_ylim([0., 1000.])
#axSpect.set_yticks(['0', '500', '1000'])
#line, = axSpect.plot(plotTime, plotData)
plotFreq = plotTime - np.pi
line, = axSpect.semilogy(plotFreq, plotData)
axSpect.set_yscale('symlog', linthreshy=PLOTWIDTH**0.5)


#### Axes for sliders ####
#axSl1 = fig.add_axes([.825, .7, .05, .275])
#axSl1.set_xticks([])
#axSl1.set_yticks([])
#axSl2 = fig.add_axes([.92, .7, .05, .275])
#axSl2.set_xticks([])
#axSl2.set_yticks([])

# Keypress 'q' to quit
def press(event):
    global ptList, data
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
    elif event.key == 'backspace':
        if len(ptList) > 0:
            lastPt = ptList.pop()
            lastPt['circle'].remove()
            fig.canvas.draw()
            updateWave()

########################
def on_press(event):
    global buttonState, selectedPt
#    print 'In on_press()'
    inAPoint = False
    for pt in ptList:
        contains, attrd = pt['circle'].contains(event)
        if contains:
            inAPoint = True
            if pt['selected']:
                pt['selected'] = False
                pt['circle'].set_fc('blue')
            else:
                pt['selected'] = True
                selectedPt = pt
                pt['circle'].set_fc('red')
            fig.canvas.draw()
            break
    buttonState = True
    
    if not inAPoint:
        xdata = event.xdata
        ydata = event.ydata
        circ = mpatches.Circle((xdata, ydata), ptRad)
        ax.add_patch(circ)
        ptList.append({'xPos':xdata,
                       'yPos':ydata,
                       'selected':True,
                       'circle':circ})
        selectedPt = ptList[-1]
        updateWave()

########################    
def on_release(event):
    global buttonState, selectedPt
#    print 'In on_release()'
    for pt in ptList:
        #contains, attrd = pt['circle'].contains(event)
        if pt['selected']:
            xdata = event.xdata
            ydata = event.ydata
            pt['circle'].center = (xdata, ydata)
            buttonState = False
            pt['selected'] = False
            selectedPt = None
            pt['circle'].set_fc('blue')
            fig.canvas.draw()
    buttonState = False
    updateWave()
    
########################        
def on_motion(event):
    global xdata, ydata, selectedPt, ptList

    if buttonState:
        xdata = event.xdata
        ydata = event.ydata
        selectedPt['circle'].center = (xdata, ydata)
        selectedPt['xPos'] = xdata
        selectedPt['yPos'] = ydata
        fig.canvas.draw()
        updateWave()
   	   
    
ptList[0]['circle'] = mpatches.Circle((xdata, ydata), ptRad)
ax.add_patch(ptList[0]['circle'])

# Connect fig to events
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
fig.canvas.mpl_connect('key_press_event',       press)


# Initial update of wave
#updateWave()

# start the stream (4)
stream.start_stream()

# Show plot
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
