import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from group_possessions import group_possessions
from corsi import shot_attempts, separate_possessions_by_board
img = plt.imread(r'C:/Users/13432/Pictures/hockeyrink_rotated.png')


data = pd.read_csv('Linhac_df_keyed_20_games.csv')
possessions = group_possessions(data)
data = data[data['currentpossession'].notna()]

lpr = data[data['eventname'] == 'lpr']
xcoords = lpr['xadjcoord']
ycoords = lpr['yadjcoord']

def plot_rink():
    plt.imshow(img, extent=[-100, -25, -42.5, 42.5])
    plt.show()

#plot the density of lpr, pass No. bins to function for resolution
def lpr_density(possessions, bins):
    xcoords = []
    ycoords = []
    for possession in possessions:
        possession = pd.DataFrame(possession).reset_index(drop=True)
        #if possession has an lpr, get location of lpr
        if possession['eventname'].str.contains('lpr').any():
            lprs = possession['eventname'].str.contains('lpr')
            x = possession.loc[lprs, 'xadjcoord'].values
            y = possession.loc[lprs, 'yadjcoord'].values
            
            for i in range(len(x)):
                if (x[i] < -26):
                    xcoords.append(x[i])
                    ycoords.append(y[i])

    
    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=1.5)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='seismic')
    plt.title('LPR Frequency')
    plt.colorbar()
    plt.show() 


def possession_starts(possessions, bins):
    xcoords = []
    ycoords = []
    for possession in possessions:
        possession = pd.DataFrame(possession).reset_index(drop=True)
        x = possession.loc[0, 'xadjcoord']
        y = possession.loc[0, 'yadjcoord']
        if (x < -26):
            xcoords.append(x)
            ycoords.append(y)


    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)
    #normalize heatmap
    heatmap = gaussian_filter(heatmap, sigma=1.5)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap with mask
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='seismic')
    plt.title('Possession Start Locations')
    plt.colorbar()
    plt.show()

#get single possessions play by play
def possessions_xgs():
    #data grouped by game and possession, with possessions with no shot removed
    filtered_data = data#[data['xg'].notna()]
    groups = filtered_data.groupby(['gameid', 'currentpossession'])
   
    #store starting location, total xg of possession
    possession_xgs = groups['xg'].sum()
    possession_x, possession_y = groups.first()['xadjcoord'], groups.first()['yadjcoord']

    plt.scatter(list(possession_x), list(possession_y), list(possession_xgs), cmap = 'viridis')
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Heatmap of z values')
    plt.show()

def xg_density(possessions, bins):
    shots = shot_attempts(possessions)
    xcoords = []
    ycoords = []
    xgs = []
    i=0
    for possession in possessions:
        possession = pd.DataFrame(possession).reset_index(drop=True)
        if possession['eventname'].str.contains('lpr').any():
            lprs = possession['eventname'].str.contains('lpr')
            x = possession.loc[lprs, 'xadjcoord'].values
            y = possession.loc[lprs, 'yadjcoord'].values
            if possession['eventname'].str.contains('shot').any():
                xg = possession.loc[possession['eventname'].str.contains('shot'), 'xg'].values
                for i in range(len(xg)):
                    for j in range(len(x)):
                        if (x[j] < -26):
                            xcoords.append(x[j])
                            ycoords.append(y[j])
                            xgs.append(xg[i])

        i+=1

    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)
    shots_sum, _, _ = np.histogram2d(
        xcoords, ycoords, bins=bins, weights=xgs)
    avg_xg = np.divide(shots_sum, heatmap, out=np.zeros_like(
        shots_sum), where=heatmap != 0)
    avg_xg[np.isnan(avg_xg)] = 0
    
    avg_xg = gaussian_filter(avg_xg, sigma=2)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap
    plt.clf()
    plt.imshow(avg_xg.T, extent=extent, origin='lower', cmap='seismic')
    plt.title('Cumulative XG from Starting Location')
    plt.colorbar()
    plt.show()

def breakout_success(possessions, bins):
    xcoords = []
    ycoords = []
    breakouts = []
    i = 0
    for possession in possessions:
        possession = pd.DataFrame(possession).reset_index(drop=True)
        if possession['eventname'].str.contains('lpr').any():
            possession_breakout = possession['eventname'].str.contains('controlledexit')
            lprs = possession['eventname'].str.contains('lpr')
            x = possession.loc[lprs, 'xadjcoord'].values
            y = possession.loc[lprs, 'yadjcoord'].values
            if possession['eventname'].str.contains('controlledexit').any():
                breakout = possession.loc[possession_breakout, 'outcome'].values
                for i in range(len(breakout)):
                    for j in range(len(x)):
                        if (x[j] < -26):

                            xcoords.append(x[j])
                            ycoords.append(y[j])
                            breakouts.append(breakout[i])

        i += 1
    #net number of breakout successes
    breakout_bool = [1 if x == 'successful' else -1 for x in breakouts]


    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)
    breakout_sum, _, _ = np.histogram2d(
        xcoords, ycoords, bins=bins, weights=breakout_bool)
    avg_breakout = np.divide(breakout_sum, heatmap, out=np.zeros_like(
        breakout_sum), where=heatmap != 0)


    avg_breakout = gaussian_filter(avg_breakout, sigma=5)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap
    plt.clf()
    plt.imshow(avg_breakout.T, extent=extent, origin='lower', cmap='seismic')
    plt.title('Puck Battles Leading to Breakouts')
    plt.colorbar()
    plt.show()

def breakout_time(possessions, bins):
    xcoords = []
    ycoords = []
    breakouts = []
    times = []
    i = 0
    for possession in possessions:
        possession = pd.DataFrame(possession).reset_index(drop=True)
        if possession['eventname'].str.contains('lpr').any():
            possession_breakout = possession['eventname'].str.contains(
                'controlledexit')
            lprs = possession['eventname'].str.contains('lpr')
            x = possession.loc[lprs, 'xadjcoord'].values
            y = possession.loc[lprs, 'yadjcoord'].values
            if possession['eventname'].str.contains('controlledexit').any():
                breakout = possession.loc[possession_breakout, 'outcome'].values
                timer = possession['compiledgametime'].iloc[-1] - possession['compiledgametime'].iloc[0]
                for i in range(len(breakout)):
                    for j in range(len(x)):
                        if (x[j] < -26 and timer>0):
                            times.append(timer)
                            xcoords.append(x[j])
                            ycoords.append(y[j])
                            breakouts.append(breakout[i])

    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=bins)
    breakout_sum, _, _ = np.histogram2d(
        xcoords, ycoords, bins=bins, weights=times)
    avg_breakout = np.divide(breakout_sum, heatmap, out=np.zeros_like(
        breakout_sum), where=heatmap != 0)
    

    avg_breakout = gaussian_filter(avg_breakout, sigma=10)

    # Create extent for imshow
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot heatmap
    plt.clf()
    plt.imshow(avg_breakout.T, extent=extent, origin='lower', cmap='seismic')
    #add colorbar label


    plt.title('LPRs and Possession Time')
    cbar = plt.colorbar()
    cbar.set_label('Time of Possession (s)')
    plt.show()



a=0
# breakout_time(possessions, (60, 100))
# lpr_density(possessions, (40, 75))
# xg_density(possessions, (40, 75))
# breakout_success(possessions, (40, 75))

# possession_starts(possessions, 100)
plot_rink()
