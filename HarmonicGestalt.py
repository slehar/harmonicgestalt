# -*- coding: utf-8 -*-
"""
HarmonicGestalt.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,10))
fig.canvas.set_window_title('Harmonic Gestalt')
fig.text(.35, .92, 'Harmonic Gestalt', size=24)
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xticks([])
ax.set_yticks([])

buttonState = False
xdata, ydata = .5, .5
lastX, lastY = xdata, ydata

def on_press(event):
    global buttonState
    contains, attrd = pt.contains(event)
    if not contains:
        return
    print 'In on_press()'
    buttonState = True
    
def on_release(event):
    global buttonState
    contains, attrd = pt.contains(event)
    if not contains:
        xdata = event.xdata
        ydata = event.ydata
        buttonState = False
        pt.center = (xdata, ydata)
        fig.canvas.draw()
        return
    print 'In on_press()'
    buttonState = False
    
        
def on_motion(event):
    global pt, xdata, ydata

    contains, attrd = pt.contains(event)
    if buttonState:
        xdata = event.xdata
        ydata = event.ydata
        pt.center = (xdata, ydata)
        fig.canvas.draw()
    

pt = mpatches.Circle((xdata, ydata),.02)
ax.add_patch(pt)
pt.figure.canvas.mpl_connect('button_press_event',    on_press)
pt.figure.canvas.mpl_connect('button_release_event',  on_release)
pt.figure.canvas.mpl_connect('motion_notify_event',   on_motion)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
