# -*- coding: utf-8 -*-
"""
TstButton.py

Created on Sat Apr  8 10:23:39 2017

@author: slehar

see http://matplotlib.org/users/event_handling.html

"""
import matplotlib.pyplot as plt

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
square = plt.Rectangle((.2, .2), .2, .2, fc=(1,0,0), ec='k')
butt = ax.add_patch(square)
buttText = ax.text(.275, .29, 'OFF')
buttState = False
def on_press(event):
    global buttState
    buttState = not buttState
    if buttState:
        butt.set_fc((0,1,0))
        buttText.set_text('ON')
    else:
        butt.set_fc((1,0,0))
        buttText.set_text('OFF')
    plt.pause(.001)
    plt.show()    
butt.figure.canvas.mpl_connect('button_press_event', on_press)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
