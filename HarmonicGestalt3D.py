"""
HarmonicGestalt3D.py


"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'gray' 

#### Fugure ####
plt.close('all')
fig = plt.figure()
fig.canvas.set_window_title('HarmonicGestalt3D')

# Keypress 'q' to quit callback function
def press(event):
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)


#### Axes ####
ax = fig.gca(projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)


def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

xs = np.arange(0, 10, 0.4)

#### Polygon ####
verts = [[[0., 0.], [1., 0.], [1., 1.], [0., 1.], [0., 0.]]]
poly = PolyCollection(verts)
poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=0., zdir='y')

# Surface plot

X = np.array([.25, .75, .75, .25, .25])
Y = np.array([.25, .25, .75, .75, .25])
Z = np.array([0.3,  0.3,  0.3,  0.3,  0.3])
#ax.plot_surface(X, Y, Z, color='b', facecolors='r', shade=True)

plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
