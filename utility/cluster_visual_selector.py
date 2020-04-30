import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def box_outline_for_plot(x_range, y_range):
    return [x_range[0], x_range[1], x_range[1], x_range[0], x_range[0]], \
           [y_range[1], y_range[1], y_range[0], y_range[0], y_range[1]] 

def box_outline_plot(x_range, y_range):
    bx,by = box_outline_for_plot(x_range,y_range)
    ax = plt.gca()
    ax.fill(bx, by, color='gray', alpha=0.5) 
    plt.plot(bx,by,'k--', linewidth=.5)
    
def box_points(x,y, x_range=[], y_range=[]):
    # x cut 
    if x_range:
        x_cut = np.argwhere(
            np.logical_and(x>=x_range[0] , x<=x_range[1])).reshape(1,-1)
    if y_range:
        y_cut = np.argwhere(
            np.logical_and(y>=y_range[0] , y<=y_range[1])).reshape(1,-1)
    if x_range and y_range: 
        pass
    
    return np.intersect1d(y_cut, x_cut)