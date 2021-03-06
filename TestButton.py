# -*- coding: utf-8 -*-
"""
TestButton.py

Home-brewed button

Created on Sat Apr  8 10:23:39 2017

@author: slehar

"""
import matplotlib.pyplot as plt
#from matplotlib.widgets import Button

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('TestButton')
ax = fig.add_axes([.1, .1, .8, .8])
ax.axes.set_xticks([])
ax.axes.set_yticks([])

# Keypress 'q' to quit
def press(event):
    if event.key == 'q':
        plt.close()
fig.canvas.mpl_connect('key_press_event', press)


# Add button
axButt = fig.add_axes([.4, .4, .2, .2])
axButt.patch.set_fc('r')
axButt.axes.set_xticks([])
axButt.axes.set_yticks([])

buttText = axButt.text(.4, .45, 'OFF')
buttState = False
def on_press(event):
    global buttState, buttText
    buttState = not buttState
    if buttState:
        axButt.patch.set_fc('g')
        buttText.set_text('ON')
    else:
        axButt.patch.set_fc('r')
        buttText.set_text('OFF')
    plt.pause(.001)
    plt.show()    
axButt.figure.canvas.mpl_connect('button_press_event', on_press)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
