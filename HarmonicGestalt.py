# -*- coding: utf-8 -*-
"""
HarmonicGestalt.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from   matplotlib.widgets import Slider
import pyaudio

plt.rcParams['image.cmap'] = 'gray' 

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
ptList.append({'xPos':0., 'yPos':0., 'selected':False})
selectedPt = None
freqList = []

buttonState = False
xdata, ydata = 0., 0.

    
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
figYSize, figXSize = (15,8)
winAspect = float(figYSize)/float(figXSize)
plt.close('all')
fig = plt.figure(figsize=(figYSize,figXSize))
fig.canvas.set_window_title('Harmonic Gestalt')

#### Stimulus axes ####
axStim = fig.add_axes([.1, .4/winAspect, .7/winAspect, .75])
#axStim.set_xticks([])
#axStim.set_yticks([])
axStim.set_xlim([-1,1])
axStim.set_ylim([-1,1])
axStim.set_title('Stimulus')

#### Percept Axes #### (just to add 2d border around 3d Axes)
ax0 = fig.add_axes([.55,.2,.4,.4*winAspect])
ax0.axes.set_xticks([])
ax0.axes.set_yticks([])
ax0.set_title('Percept')

#### 3D Axes ####
ax3d = fig.add_axes([.57,.22,.38,.38*winAspect], projection='3d')
ax3d.set_xlabel('X')
ax3d.set_ylabel('Z') # swap Y and Z
ax3d.set_zlabel('Y')
ax3d.set_xlim3d(-1, 1)
ax3d.set_ylim3d(-1, 1)
ax3d.set_zlim3d(1, -1)

# Back plane
verts3D = np.array([[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],[-1,-1,1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly1 = PolyCollection(vertsXY)
poly1.set_alpha(0.7)
poly1.set_color('w')
poly1.set_edgecolor('k')
ax3d.add_collection3d(poly1, zs=vertsZ, zdir='y')

# Front plane
verts3D = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,-1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly2 = PolyCollection(vertsXY)
poly2.set_alpha(0.7)
poly2.set_color('w')
poly2.set_edgecolor('k')
ax3d.add_collection3d(poly2, zs=vertsZ, zdir='y')

#### z-rod ####
ptList[0]['rod'] = ax3d.plot([ptList[0]['xPos'], ptList[0]['xPos']], 
                             [ptList[0]['yPos'], ptList[0]['yPos']], 
                             [-1, 1], color='gray', zdir='y')
         
#### z-bead ####
ptList[0]['bead'] = ax3d.scatter([ptList[0]['xPos']], [ptList[0]['xPos']], 
                                 [0.], zdir='y', color='gray')

#### Axes for spectrum ####
axSpect = fig.add_axes([.1, .05/winAspect, .7/winAspect, .15])
axSpect.set_xlim([-3., 3.])
axSpect.set_ylim([0., 1000.])
plotFreq = plotTime - np.pi
line, = axSpect.semilogy(plotFreq, plotData)
axSpect.set_yscale('symlog', linthreshy=PLOTWIDTH**0.5)

#### Axes for sliders ####
axSl0 = fig.add_axes([.6, .15, .6/winAspect, .02])
axSl0.set_xticks([])
axSl0.set_yticks([])
slider0 = Slider(axSl0, '0', -1., 1., valinit=0.)
ptList[0]['depth'] = slider0.val

def update0(val):
    depth = slider0.val
    print 'depth = %5.2f'%depth
#    ptList[0]['bead']
slider0.on_changed(update0)


# Keypress 'q' to quit
def press(event):
    global ptList, data
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
    elif event.key == 'm':
        stream.stop_stream()
        stream.close()
        pa.terminate()
    elif event.key == 'backspace':
        if len(ptList) > 0:
            lastPt = ptList.pop()
            lastPt['circle'].remove()
            fig.canvas.draw()
            updateWave()

########################
def on_press(event):
    global buttonState, selectedPt
    if event.inaxes is not axStim:
        return
    print 'event pos %5.2f, %5.2f'%(event.xdata,event.ydata)
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
        circ = mpatches.Circle((ydata, xdata), ptRad)
        axStim.add_patch(circ)
        ptList.append({'xPos':xdata,
                       'yPos':ydata,
                       'selected':True,
                       'circle':circ})
        ax3d.plot([ptList[-1]['xPos'], ptList[-1]['xPos']], 
                  [-ptList[-1]['yPos'], -ptList[-1]['yPos']], 
                  [-1, 1], zdir='y', color='gray')
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
   	   

# Plot zeroth point    
ptList[0]['circle'] = mpatches.Circle((xdata, ydata), ptRad)
axStim.add_patch(ptList[0]['circle'])

plt.sca(axStim)

# Connect fig to events
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
fig.canvas.mpl_connect('key_press_event',       press)


# Initial update of wave
#updateWave()

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
