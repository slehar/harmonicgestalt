"""
Test3DPlot.py

"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'gray' 

#### Figure ####
plt.close('all')
fig = plt.figure()
fig.canvas.set_window_title('Test3DPlot')

# Keypress 'q' to quit callback function
def press(event):
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

#### Axes ####
ax = fig.gca(projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Z') # swap Y and Z
ax.set_zlabel('Y')

ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)


#### Polygon1 ####
# 2D [[x,y]...] and 1D [z...]
verts1 = [[[-1,-1], [1., -1], [1., 1.], [-1, 1.], [-1,-1]]]
poly1 = PolyCollection(verts1)
poly1.set_alpha(0.7)
poly1.set_color('r')
zs=[-1,-1,1,1,-1]
ax.add_collection3d(poly1, zs=zs, zdir='y')

#### Polygon2 ####
# 3D [[x,y,z]...] list
verts3D = np.array([[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0],[-1,-1,0]])

# Split 3D [[x,y,z]...] list into 2D [[x,y]...] and 1D [z...]
vertsXY = [[[verts3D[i][0], verts3D[i][1]] for i in range(len(verts3D))]]
vertsZ  = [  verts3D[i][2]                 for i in range(len(verts3D))]

poly2 = PolyCollection(vertsXY)
poly2.set_alpha(0.7)
poly2.set_color('g')
ax.add_collection3d(poly2, zs=vertsZ, zdir='y')

plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
