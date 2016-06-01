# -*- coding: utf-8 -*-
"""
HarmonicGestalt.py

Created on Wed Jun  1 09:45:43 2016

@author: slehar
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#import matplotlib.lines as mlines
from matplotlib import animation
#from matplotlib.widgets import CheckButtons
#from vertslider import VertSlider

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,10))
fig.canvas.set_window_title('Harmonic Gestalt')
fig.text(.35, .92, 'Harmonic Gestalt', size=24)
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xticks([])
ax.set_yticks([])

pt = mpatches.Circle((.5,.5),.02)
ax.add_patch(pt)



# The animation function (evaluated repeatedly and endlessly)
#def animate(num):
#    pass


# Matplotlib animation funcion calls animate()    
#anim = animation.FuncAnimation(fig, animate, 
#                               repeat=True,
#                               interval=0)

# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
