import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

data = pd.read_csv('Linhac_df_keyed_20_games.csv')
data = data[data['currentpossession'].notna()]

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

#get rows where possession changes occur, returns boolean array
def possession_changes():
    data['prev_possession'] = data['currentpossession'].shift()

    data['possession_change'] = (data['currentpossession'] != data['prev_possession']).astype(int)
    return data['possession_change'] == 1

#get single possessions play by play
def possessions_xgs():
    groups = data.groupby(['gameid', 'currentpossession'])

    #store starting location, total xg of possession
    possession_xgs = groups['xg'].sum()
    possession_x, possession_y = groups.first()['xadjcoord'], groups.first()['yadjcoord']

    plt.scatter(list(possession_x), list(possession_y), list(possession_xgs), cmap = 'viridis')
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Heatmap of z values')
    plt.show()

possessions_xgs()
a=0
