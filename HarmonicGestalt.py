# -*- coding: utf-8 -*-
"""
HarmonicGestalt.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ptRad = .01

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(8,8))
fig.canvas.set_window_title('Harmonic Gestalt')
fig.text(.35, .92, 'Harmonic Gestalt', size=24)
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xticks([])
ax.set_yticks([])

ptList = []
ptList.append({'xPos':.5, 'yPos':.5, 'selected':False})
selectedPt = None

buttonState = False
xdata, ydata = .5, .5

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
    
########################        
def on_motion(event):
    global xdata, ydata

    print 'In on_motion()'
    if buttonState:
        xdata = event.xdata
        ydata = event.ydata
        selectedPt['circle'].center = (xdata, ydata)
        fig.canvas.draw()
    
print 'init done'
ptList[0]['circle'] = mpatches.Circle((xdata, ydata), ptRad)
ax.add_patch(ptList[0]['circle'])
print 'patch added'
fig.canvas.mpl_connect('button_press_event',    on_press)
fig.canvas.mpl_connect('button_release_event',  on_release)
fig.canvas.mpl_connect('motion_notify_event',   on_motion)
print 'events connected'


# Show plot
plt.show()
print 'showed!'
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
