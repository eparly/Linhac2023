import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Linhac_df_keyed_20_games.csv')

lpr = data[data['eventname'] == 'lpr']
xcoords = lpr['xadjcoord']
ycoords = lpr['yadjcoord']

#plot the density of lpr, pass No. bins to function for resolution
def lpr_density(bins):
    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.colorbar()
    plt.show()

    
    
a=0
