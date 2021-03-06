# -*- coding: utf-8 -*-
"""
HarmonicGestalt3dSlide.py

Created on Tue Apr 4 2017

@author: slehar
"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from   matplotlib.widgets import Slider
from   matplotlib.widgets import RadioButtons
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
depth = 0
delDepth = 0.1

ptList = []
lineList = []
rotList = []
line2DList = []
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
                       (ptList[0]['zPos']  - ptList[1]['zPos'])**2.)
        freqList.append(int(BASEFREQ/dist))
    else:
        for point1 in ptList:
            for point2 in ptList:
                if point1 is not point2:
                    dist = np.sqrt((point1['xPos']  - point2['xPos'])**2. +
                                   (point1['yPos']  - point2['yPos'])**2. +
                                   (point1['zPos']  - point2['zPos'])**2.)
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
#figYSize, figXSize = (12,6)
winAspect = float(figYSize)/float(figXSize)
plt.close('all')
fig = plt.figure(figsize=(figYSize,figXSize))
fig.canvas.set_window_title('Harmonic Gestalt 3D Slide')
fig.text(.008/winAspect, .9, 'click new point\ndrag move point')
fig.text(.008/winAspect, .7, 'del : delete pt\n\nm : mute\n\nq : quit')

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

#### Depth Slider  ####
axSl = fig.add_axes([.55, .1, .4, .05])
axSl.axes.set_xticks([])
axSl.axes.set_yticks([])
slider1 = Slider(axSl, 'depth', -2., 2., valinit=0.)
depth = slider1.val

#### << < || > >>  play buttons ####
xCoords = np.linspace(.55, .91, num=5)
playButt0 = fig.add_axes([xCoords[0], .05, .04, .04])
playButt0.axes.set_xticks([]), playButt0.axes.set_yticks([])

playButt1 = fig.add_axes([xCoords[1], .05, .04, .04])
playButt1.axes.set_xticks([]), playButt1.axes.set_yticks([])

playButt2 = fig.add_axes([xCoords[2], .05, .04, .04])
playButt2.axes.set_xticks([]), playButt2.axes.set_yticks([])

playButt3 = fig.add_axes([xCoords[3], .05, .04, .04])
playButt3.axes.set_xticks([]), playButt3.axes.set_yticks([])

playButt4 = fig.add_axes([xCoords[4], .05, .04, .04])
playButt4.axes.set_xticks([]), playButt4.axes.set_yticks([])

playText0 = playButt0.text(.3, .3, '<<')
playText1 = playButt1.text(.3, .3, '<' )
playText2 = playButt2.text(.3, .3, '||')
playText3 = playButt3.text(.3, .3, '>' )
playText4 = playButt4.text(.3, .3, '>>')
    
def on_playButt(event):
    global depth, delDepth
    
    if (event.inaxes is playButt0):
        for d in np.arange(2, -2, -.1):
            depth = d
            update(depth)
            slider1.set_val(depth)
    if (event.inaxes is playButt1):
        depth -= delDepth
        depth = max(depth, slider1.valmin)
        slider1.set_val(depth)
    if (event.inaxes is playButt2):
        depth = 0
        slider1.set_val(depth)
    if (event.inaxes is playButt3):
        depth += delDepth
        depth = min(depth, slider1.valmax)
        slider1.set_val(depth)
    if (event.inaxes is playButt4):
        for d in np.arange(-2, 2, .1):
            depth = d
            update(depth)
            slider1.set_val(depth)    
fig.canvas.mpl_connect('button_press_event', on_playButt)
    
# Back plane
verts3D = np.array([[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],[-1,-1,1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly1 = PolyCollection(vertsXY)
poly1.set_alpha(0.2)
poly1.set_color('w')
poly1.set_edgecolor('k')
ax3d.add_collection3d(poly1, zs=vertsZ, zdir='y')

# Front plane
verts3D = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,-1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly2 = PolyCollection(vertsXY)
poly2.set_alpha(0.5)
poly2.set_color('w')
poly2.set_edgecolor('k')
ax3d.add_collection3d(poly2, zs=vertsZ, zdir='y')

# Necker Radiobuttons
rax = plt.axes([0.005, 0.25, 0.16/winAspect, 0.4])
radio = RadioButtons(rax, ['Clear', 'Nek0', 'Nek1', 'Nek2', 'Nek3', 'Nek4'])

def addPoint(xyz):
    xPos, yPos, zPos = xyz[0], xyz[1], xyz[2]
    circle = mpatches.Circle((xPos, yPos), ptRad)
    axStim.add_patch(circle)
#    rod  = ax3d.plot([xPos, xPos], [-yPos, -yPos], [-1, 1], color='gray', zdir='y')
    rod  = ax3d.plot([xPos, xPos], [yPos, yPos], [-1, 1], color='gray', zdir='y')
    bead = ax3d.scatter([xPos], [-yPos], [zPos], zdir='y', color='blue')
    bead.set_offsets([xPos, yPos])
    bead.set_3d_properties(zPos, zdir='y')
    ptList.append({'xPos':xPos, 
                   'yPos':yPos, 
                   'zPos':zPos,
                   'selected':False,
                   'circle':circle, 
                   'rod':rod, 
                   'bead':bead})

def addLine(pt1, pt2, color='k'):
    x1, x2 = pt1[0], pt2[0]
    y1, y2 = pt1[1], pt2[1]
    z1, z2 = pt1[2], pt2[2]
    line = ax3d.plot([x1, x2], [y1, y2], [z1, z2], color=color, zdir='y')
    return line
    
def addLine2D(pt1, pt2, color='k'):
    x1, x2 = pt1[0], pt2[0]
    y1, y2 = pt1[1], pt2[1]
    line2D = axStim.plot([x1, x2], [y1, y2], color=color)
    return line2D

def update(depth):   
    global rotList, ptList, lineList, line2DList
    
    # clear points, lines, and 2D lines
    for pt in ptList:
        pt['circle'].remove()
        pt['rod'].pop(0).remove()
        pt['bead'].remove()
        ptList = ptList[1:]
    for line in lineList:
        if line[0]:
            line[0].remove()
    lineList = []
    for line2D in line2DList:
        if line2D[0]:
            line2D[0].remove()
    line2DList = []
            
    if len(rotList) > 0:
        scaList = np.array(rotList)
        scaList[:,2] *= depth
    else: 
        scaList = np.array([])
    
    if len(scaList) > 0:        
        for pt in scaList:
            addPoint(pt)
            
        # Add 3-D lines from points 0 > 1 > 2 > 3 > 0 (front square)  
        lineList.append(addLine(scaList[0], scaList[1], color='r'))            
        lineList.append(addLine(scaList[1], scaList[2], color='r'))            
        lineList.append(addLine(scaList[2], scaList[3], color='r'))            
        lineList.append(addLine(scaList[3], scaList[0], color='r'))
                
        # Add 3-D lines from points 4 > 5 > 6 > 7 > 4 (back square)  
        lineList.append(addLine(scaList[4], scaList[5]))            
        lineList.append(addLine(scaList[5], scaList[6]))            
        lineList.append(addLine(scaList[6], scaList[7]))            
        lineList.append(addLine(scaList[7], scaList[4])) 
               
        # Add 3-D lines from points 0 > 4, 1 > 5, 2 > 6, 3 > 7 (joining lines)  
        lineList.append(addLine(scaList[0], scaList[4]))            
        lineList.append(addLine(scaList[1], scaList[5]))            
        lineList.append(addLine(scaList[2], scaList[6]))            
        lineList.append(addLine(scaList[3], scaList[7]))            
                
        # Add 2-D projection from points 0 > 1 > 2 > 3 > 0 (front square)  
        line2DList.append(addLine2D(scaList[0], scaList[1], color='r'))            
        line2DList.append(addLine2D(scaList[1], scaList[2], color='r'))            
        line2DList.append(addLine2D(scaList[2], scaList[3], color='r'))            
        line2DList.append(addLine2D(scaList[3], scaList[0], color='r'))
                
        # Add 2-D projection from points 4 > 5 > 6 > 7 > 4 (back square)  
        line2DList.append(addLine2D(scaList[4], scaList[5]))            
        line2DList.append(addLine2D(scaList[5], scaList[6]))            
        line2DList.append(addLine2D(scaList[6], scaList[7]))            
        line2DList.append(addLine2D(scaList[7], scaList[4])) 
               
       # Add 2-D projection from points0 > 4, 1 > 5, 2 > 6, 3 > 7 (joining lines)  
        line2DList.append(addLine2D(scaList[0], scaList[4]))            
        line2DList.append(addLine2D(scaList[1], scaList[5]))            
        line2DList.append(addLine2D(scaList[2], scaList[6]))            
        line2DList.append(addLine2D(scaList[3], scaList[7]))    
        
    plt.show()
    plt.pause(.001)
    updateWave()
    plt.draw()    

def updateSl1(val):
    global depth, delDepth    
    depth = slider1.val
    update(depth)
slider1.on_changed(updateSl1)


# Frontal cube              

d = .5
frontal = [[-d, -d, -d],
           [ d, -d, -d],
           [ d,  d, -d],
           [-d,  d, -d],
           [-d, -d,  d],
           [ d, -d,  d],
           [ d,  d,  d],
           [-d,  d,  d]]
        
def rotateX(cube, aX):    
    cosX, sinX = np.cos(np.deg2rad(aX)), np.sin(np.deg2rad(aX))    
    rotX = [[1,       0.,    0.],
            [0,     cosX, -sinX],
            [0,     sinX,  cosX]]                        
    return np.matmul(cube, rotX)
    
def rotateY(cube, aY):    
    cosY, sinY = np.cos(np.deg2rad(aY)), np.sin(np.deg2rad(aY))    
    rotY = [[ cosY,   0.,  sinY],
            [   0.,   1.,    0.],
            [-sinY,   0.,  cosY]]            
    return np.matmul(cube, rotY)

def rotateZ(cube, aZ):    
    cosZ, sinZ = np.cos(np.deg2rad(aZ)), np.sin(np.deg2rad(aZ))    
    rotZ = [[cosZ, -sinZ, 0.],
            [sinZ,  cosZ,  0.],
            [  0.,    0.,  1.]]
    return np.matmul(cube, rotZ)


# radio button callback function to switch Necker pattern
def setPattern(label):
    global ptList, lineList, rotList, line2DList
    
    if label == 'Clear':
        rotList = []
        for pt in ptList:
            if pt['circle']:
                pt['circle'].remove()
            if pt['rod']:
                pt['rod'][0].remove()
            if pt['bead']:
                pt['bead'].remove()
        ptList = []
    elif label == 'Nek0':
        rotList = frontal
    elif label == 'Nek1':
        rotList = rotateY(frontal,  -22)
        rotList = rotateX(rotList,  22)
    elif label == 'Nek2':
        rotList = rotateY(frontal,  -45)
        rotList = rotateX(rotList,   45)
    elif label == 'Nek3':
        rotList = rotateY(frontal,  -45)
        rotList = rotateX(rotList,   30)
    elif label == 'Nek4':
        rotList = rotateY(frontal,  -45)
        rotList = rotateX(rotList,   35.2)        
    update(depth)    
radio.on_clicked(setPattern)


#### Axes for spectrum ####
axSpect = fig.add_axes([.1, .05/winAspect, .7/winAspect, .15])
axSpect.set_xlim([-2., 2.])
axSpect.set_ylim([0., 1000.])
plotFreq = plotTime - np.pi
line, = axSpect.semilogy(plotFreq, plotData)
axSpect.set_yscale('symlog', linthreshy=PLOTWIDTH**0.5)

# Keypress 'q' to quit
def keypress(event):
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
#        label = 'Pt %1d'%len(ptList)
        xdata = event.xdata
        ydata = event.ydata
        plt.sca(axStim)
        circle = mpatches.Circle((xdata, ydata), ptRad) # 2D point in axStim
        axStim.add_patch(circle)
        plt.sca(ax3d)

        rod  = ax3d.plot([xdata, xdata], [-ydata, -ydata], [-1, 1], color='gray', zdir='y')
        bead = ax3d.scatter([xdata], [-ydata], [0.], zdir='y', color='blue')
        depth = 0.

        ptList.append({'xPos':xdata, 
                       'yPos':ydata, 
                       'selected':False,
                       'circle':circle, 
                       'rod':rod, 
                       'bead':bead, 
                       'zPos':depth})
               
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
        selectedPt['bead'].set_3d_properties(ptList[0]['zPos'], zdir='y')
        plt.pause(.001)
#        fig.canvas.draw()
        updateWave()
   	   

plt.sca(axStim)

# Connect fig to events
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
fig.canvas.mpl_connect('key_press_event',       keypress)


# Show plot
plt.show()

# Gef fig manager to raise window in top left corner (10,10)
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
