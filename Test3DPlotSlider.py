"""
Test3DPlot.py

"""

from mpl_toolkits.mplot3d import Axes3D # Required only for its side-effect
#del Axes3D      # to allow "projection='3d'", thus deleted because unused
from matplotlib.widgets import Slider
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
ax.view_init(30, -45)

ax.set_xlabel('X')
ax.set_ylabel('Z') # swap Y and Z
ax.set_zlabel('Y')

ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)

# Slider
axSlider1 = fig.add_axes([0.1, 0.1, 0.4, 0.04])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

slider1 = Slider(axSlider1, 'depth', -1, 1, valinit=1)
depth = slider1.val

def update1(val):
    global depth
#    print 'in update'
    depth = slider1.val
    mDot[0].set_data([.5, -.2])
    mDot[0].set_3d_properties(depth, zdir='y')
#    plt.show()
    plt.pause(.001)
    
slider1.on_changed(update1)

# Back plane
verts3D = np.array([[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],[-1,-1,1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly1 = PolyCollection(vertsXY)
poly1.set_alpha(0.7)
poly1.set_color('w')
poly1.set_edgecolor('k')
ax.add_collection3d(poly1, zs=vertsZ, zdir='y')

# Front plane
verts3D = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,-1]])
vertsXY = [verts3D[:,:2]]
vertsZ  = verts3D[:,2]
poly2 = PolyCollection(vertsXY)
poly2.set_alpha(0.7)
poly2.set_color('w')
poly2.set_edgecolor('k')
ax.add_collection3d(poly2, zs=vertsZ, zdir='y')

# Points
pts = [[0,.7,-1],
       [0,.7, 1],
       [.5,-.2,-1],
       [.5,-.2, 1],
       [-.5,-.2,-1],
       [-.5,-.2, 1]]
       
npPts = np.array(pts)
swapPts = np.array([[npPts[i][0],npPts[i][2],npPts[i][1]] for i in range(len(npPts))])
ax.scatter(swapPts[:,0], swapPts[:,1], swapPts[:,2])

# Lines
xs = [pts[0][0],pts[1][0]]
ys = [pts[0][2],pts[1][2]]   # swapping y and z
zs = [pts[0][1],pts[1][1]]

line1 = ax.plot(xs, ys, zs, color=[.8,.8,.8])

xs = [pts[2][0],pts[3][0]]
ys = [pts[2][2],pts[3][2]]   # swapping y and z
zs = [pts[2][1],pts[3][1]]

line2 = ax.plot(xs, ys, zs, color=[.8,.8,.8])

xs = [pts[4][0],pts[5][0]]
ys = [pts[4][2],pts[5][2]]   # swapping y and z
zs = [pts[4][1],pts[5][1]]

line3 = ax.plot(xs, ys, zs, color=[.8,.8,.8])

# Moving dot
#mDot = ax.scatter([.5],[0], [-.2], color='r')
mDot = ax.plot([.5], [1.], [-.2], 'o', color='r')

plt.show()

# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
