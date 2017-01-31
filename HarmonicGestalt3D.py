"""
HarmonicGestalt3D.py


"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

import matplotlib

plt.rcParams['image.cmap'] = 'gray' 

#### Figure ####
figYSize, figXSize = (15,8)
winAspect = float(figYSize)/float(figXSize)

plt.close('all')
fig = plt.figure(figsize=(figYSize,figXSize))
fig.canvas.set_window_title('HarmonicGestalt3D')

# Keypress 'q' to quit callback function
def press(event):
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)


#### Stimulus Axes ####
ax   = fig.add_axes([.05,.2,.4,.4*winAspect])
ax.axes.set_xticks([])
ax.axes.set_yticks([])
ax.set_title('Stimulus')

#### Percept Axes ####
ax0 = fig.add_axes([.55,.2,.4,.4*winAspect])
ax0.axes.set_xticks([])
ax0.axes.set_yticks([])
ax0.set_title('Percept')

#### 3D Axes ####
ax3d = fig.add_axes([.57,.22,.38,.38*winAspect], projection='3d')
ax3d.set_xlabel('X')
ax3d.set_ylabel('Y')
ax3d.set_zlabel('Z')
ax3d.set_xlim3d(-1, 1)
ax3d.set_ylim3d(-1, 1)
ax3d.set_zlim3d(-1, 1)

def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

xs = np.arange(0, 10, 0.4)

#### Polygon ####
verts = [[[0., 0.], [1., 0.], [1., 1.], [0., 1.], [0., 0.]]]
poly = PolyCollection(verts)
poly.set_alpha(0.7)
ax3d.add_collection3d(poly, zs=0., zdir='y')

# Surface plot

X = np.array([.25, .75, .75, .25, .25])
Y = np.array([.25, .25, .75, .75, .25])
Z = np.array([0.3,  0.3,  0.3,  0.3,  0.3])
#ax3d.plot_surface(X, Y, Z, color='b', facecolors='r', shade=True)

plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
