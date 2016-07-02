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

ptRad     = .01      # Radius of points
RATE      = 44100    # bytes per second data rate
BASEFREQ  = 500      # base frequency Hz
CHUNK     = 8192     # frames per buffer 

# global variables
twoPi = float(2.0*np.pi)
data  = np.zeros(RATE, dtype=float)
time  = np.linspace(0, twoPi, RATE)
fData = []

ptList = []
ptList.append({'xPos':.5, 'yPos':.5, 'selected':False})
selectedPt = None
freqList = []

buttonState = False
xdata, ydata = .5, .5

# Update Wave to be played based on current slider positions
def updateWave():
    global data, fData, time, ptList, freqList

    freqList = []
    print 'In updateWave1: freqList = %r'%freqList                    

    if len(ptList) < 2:
        print 'len(ptList < 2)'
        return
    elif len(ptList) == 2:
        print 'len(ptList == 2)'
        dist = np.sqrt((ptList[0]['xPos'] - ptList[1]['xPos'])**2. +
                       (ptList[0]['yPos'] - ptList[1]['yPos'])**2.)
        freqList.append(BASEFREQ/dist)
    else:
        print 'len(ptList > 2)'
        for point1 in ptList:
            for point2 in ptList:
                if point1 is not point2:
                    dist = np.sqrt((point1['xPos'] - point2['xPos'])**2. +
                                   (point1['yPos'] - point2['yPos'])**2.)
                    print '  dist = %5.2f'%dist
                    freqList.append(BASEFREQ/dist)
                    
    print 'In updateWave2: freqList = %r'%freqList                    
                    
    fData = np.zeros(RATE, dtype=float)
    for freq in freqList:
        fData += np.sin(time*freq)
    fData = fData / np.max(np.abs(fData)) * 127 + 128
#    lastTime = time[-1] + 1./float(RATE)
#    time = np.linspace(lastTime, lastTime+1., RATE)
    data = np.uint8(fData)
    
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

# Keypress 'q' to quit
def press(event):
    sys.stdout.flush()
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        raise Exception('exit')
#        sys.exit()

# Open figure and set axes 1 for drawing Artists
#plt.close('all')
fig = plt.figure(figsize=(8,8))
fig.canvas.set_window_title('Harmonic Gestalt')
fig.text(.35, .92, 'Harmonic Gestalt', size=24)
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xticks([])
ax.set_yticks([])


# Connect fig to keypress callback function
fig.canvas.mpl_connect('key_press_event', press)

########################
def on_press(event):
    global buttonState, selectedPt
    print 'In on_press()'
    inAPoint = False
    for pt in ptList:
        contains, attrd = pt['circle'].contains(event)
        if contains:
            inAPoint = True
            print '  Contains!'
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
        print '*** NEW POINT !***'
        xdata = event.xdata
        ydata = event.ydata
        circ = mpatches.Circle((xdata, ydata), ptRad)
        ax.add_patch(circ)
        ptList.append({'xPos':xdata, 'yPos':ydata, 'selected':True,
                       'circle':circ})
        selectedPt = ptList[-1]
        updateWave()

########################    
def on_release(event):
    global buttonState, selectedPt
    print 'In on_release()'
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
        print 'In on_motion buttonstate = True'
        xdata = event.xdata
        ydata = event.ydata
        selectedPt['circle'].center = (xdata, ydata)
        selectedPt['xPos'] = xdata
        selectedPt['yPos'] = ydata
        fig.canvas.draw()
        updateWave()
   	   
    
print 'init done'
ptList[0]['circle'] = mpatches.Circle((xdata, ydata), ptRad)
ax.add_patch(ptList[0]['circle'])
print 'patch added'
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
print 'events connected'


# Initial update of wave
print 'freqList = %r'%freqList
print 'Call updateWave'
updateWave()
print 'freqList = %r'%freqList

# start the stream (4)
print 'Start stream'
stream.start_stream()

# Show plot
plt.show()
print 'Plot showed!'
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
