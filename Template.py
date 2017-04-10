# -*- coding: utf-8 -*-
"""
Template.py

Created on Sat Apr  8 10:23:39 2017

@author: slehar
"""
import matplotlib.pyplot as plt


# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('Template')
ax = fig.add_axes([.1, .1, .8, .8])
ax.axes.set_xticks([])
ax.axes.set_yticks([])

# Keypress 'q' to quit
def press(event):
    if event.key == 'q':
        plt.close()
fig.canvas.mpl_connect('key_press_event', press)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
