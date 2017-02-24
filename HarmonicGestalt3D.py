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
plotTime = np.arange(0, twoPi, twoPi/PLOTWIDTH)
plotData = np.zeros_like(plotTime)
mute = False

ptList = []
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
        dist = np.sqrt((ptList[0]['xPos']  - ptList[1]['xPos'])**2. +
                       (ptList[0]['yPos']  - ptList[1]['yPos'])**2. +
                       (ptList[0]['depth'] - ptList[1]['depth'])**2.)
        freqList.append(int(BASEFREQ/dist))
    else:
        for point1 in ptList:
            for point2 in ptList:
                if point1 is not point2:
                    dist = np.sqrt((point1['xPos']  - point2['xPos'])**2. +
                                   (point1['yPos']  - point2['yPos'])**2. +
                                   (point1['depth'] - point2['depth'])**2.)
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
fig.text(.008/winAspect, .9, 'click new point\ndrag move point')
fig.text(.008/winAspect, .7, 'd : delete pt\n\nm : mute\n\nq : quit')

#### Stimulus axes ####
axStim = fig.add_axes([.1, .4/winAspect, .7/winAspect, .75])
axStim.set_xticks([])
axStim.set_yticks([])
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

# Create zeroth point
label = 'Pt %1d'%len(ptList)
xPos, yPos = -.5, -.2
circle = mpatches.Circle((xPos, yPos), ptRad)
axStim.add_patch(circle)
rod  = ax3d.plot([xPos, xPos], [-yPos, -yPos], [-1, 1], color='gray', zdir='y')
bead = ax3d.scatter([xPos], [-yPos], [0.], zdir='y', color='blue')
yOff = 0.; deltaY = -.03
sliderAx = fig.add_axes([.6, .15+yOff, .6/winAspect, .02])
yOff += deltaY
sliderAx.set_xticks([]); sliderAx.set_yticks([])
slider = Slider(sliderAx, label, -1., 1., valinit=0.)
depth = slider.val

ptList.append({'label':label, 
               'xPos':xPos, 
               'yPos':yPos, 
               'selected':False,
               'circle':circle, 
               'rod':rod, 
               'bead':bead, 
               'depth':depth,
               'sliderAx':sliderAx, 
               'slider':slider,})
                                             
def updateSliders(val):
    for pt in ptList:
        depth = pt['slider'].val
        pt['depth'] = depth
        pt['bead'].set_offsets([pt['xPos'], -pt['yPos']])
        pt['bead'].set_3d_properties(depth, zdir='y')
        updateWave()
slider.on_changed(updateSliders)
               

#### Axes for spectrum ####
axSpect = fig.add_axes([.1, .05/winAspect, .7/winAspect, .15])
axSpect.set_xlim([-2., 2.])
axSpect.set_ylim([0., 1000.])
plotFreq = plotTime - np.pi
line, = axSpect.semilogy(plotFreq, plotData)
axSpect.set_yscale('symlog', linthreshy=PLOTWIDTH**0.5)

# Keypress 'q' to quit
def press(event):
    global ptList, data, mute
    if event.key == 'q':
        stream.stop_stream()
        stream.close()
        pa.terminate()
        plt.close()
    elif event.key == 'm':
        if mute:
            mute = False
            stream.start_stream()
        else:
            mute = True
            stream.stop_stream()
    elif event.key == 'backspace':
        if len(ptList) > 0:
            lastPt = ptList.pop()
            lastPt['circle'].remove()
            lastPt['rod'].pop(0).remove()
            lastPt['bead'].remove()
            fig.canvas.draw()
            updateWave()

########################
def on_press(event):
    global buttonState, selectedPt, yOff
    if event.inaxes is not axStim:
        return
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
        label = 'Pt %1d'%len(ptList)
        xdata = event.xdata
        ydata = event.ydata
        plt.sca(axStim)
        circle = mpatches.Circle((xdata, ydata), ptRad) # 2D point in axStim
        axStim.add_patch(circle)
        plt.sca(ax3d)

        rod  = ax3d.plot([xdata, xdata], [-ydata, -ydata], [-1, 1], color='gray', zdir='y')
        bead = ax3d.scatter([xdata], [-ydata], [0.], zdir='y', color='blue')
        sliderAx = fig.add_axes([.6, .15+yOff, .6/winAspect, .02])
        yOff += deltaY
        sliderAx.set_xticks([]); sliderAx.set_yticks([])
        slider = Slider(sliderAx, label, -1., 1., valinit=0.)
        depth = slider.val
        slider.on_changed(updateSliders)

        ptList.append({'label':label,
                       'xPos':xdata, 
                       'yPos':ydata, 
                       'selected':False,
                       'circle':circle, 
                       'rod':rod, 
                       'bead':bead, 
                       'depth':depth,
                       'sliderAx':sliderAx, 
                       'slider':slider,})
               
        selectedPt = ptList[-1]
        updateWave()
        plt.pause(.001)
        plt.show()

########################    
def on_release(event):
    global buttonState, selectedPt
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
        selectedPt['rod'][0].set_xdata([xdata, xdata])
        selectedPt['rod'][0].set_ydata([-ydata, -ydata])
        selectedPt['rod'][0].set_3d_properties([-1, 1], zdir='y')
        selectedPt['bead'].set_offsets([xdata, -ydata])
        selectedPt['bead'].set_3d_properties(ptList[0]['depth'], zdir='y')
        plt.pause(.001)
#        fig.canvas.draw()
        updateWave()
   	   

plt.sca(axStim)

# Connect fig to events
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
fig.canvas.mpl_connect('key_press_event',       press)


# Show plot
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
