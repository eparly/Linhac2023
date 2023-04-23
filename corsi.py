import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from group_possessions import group_possessions
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter

data = pd.read_csv('Linhac_df_keyed_20_games.csv')
possessions = group_possessions(data)

# find the number of shot attempts in each possession
def shot_attempts(possessions):
    shot_attempts = []
    for possession in possessions:
        count = 0
        for event in possession:
            if event['eventname'] == 'shot':
                count += 1
        shot_attempts.append(count)
    return shot_attempts

#plot the number of shots based on where the possession started using color to indicate number of shots
#only plot the possessions with at least one shot
def plot_numShots(possessions):
    shots = shot_attempts(possessions)
    xcoords = []
    ycoords = []
    i=0
    xcount=0
    for possession in possessions:
        if shots[i] > 1:
            xcoords.append(possession[0]['xadjcoord'])
            ycoords.append(possession[0]['yadjcoord'])
        i+=1
    multishots = [x for x in shots if x > 1]
    plt.scatter(xcoords, ycoords, c = multishots, cmap = 'viridis', norm=plt.Normalize(0, 5))
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Corsi of Possessions Starting Locations')
    plt.show()

#plot the average number of shots based on where the possession started, using a 2d histogram, pass number of bins to function for resolution
def corsiDensity(possessions, resolution):
    shots = shot_attempts(possessions)
    xcoords = []
    ycoords = []
    multishots = []
    i=0
    xcount=0
    for possession in possessions:
        if shots[i] > 0:
            if(possession[0]['xadjcoord']<0):
                xcoords.append(possession[0]['xadjcoord'])
                ycoords.append(possession[0]['yadjcoord'])
                multishots.append(shots[i])
        i+=1

    heatmap, xedges, yedges = np.histogram2d(xcoords, ycoords, bins=resolution)
    shots_sum, _, _ = np.histogram2d(xcoords, ycoords, bins=resolution, weights = multishots)
    avg_shots = np.divide(shots_sum, heatmap, out=np.zeros_like(shots_sum), where=heatmap!=0)

    # Smooth the heatmap
    # avg_shots = gaussian_filter(shots_sum, sigma=1)
    avg_shots = gaussian_filter(avg_shots, sigma=1)

    # Create hexbin plot
    plt.imshow(avg_shots, extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', cmap='seismic')
    # Add colorbar and axis labels
    plt.colorbar(label='Average Shots')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')

    # Show the plot
    plt.show()


def separate_possessions_by_board(possessions):
    board_range = 10  # units away from boards to consider
    board_coords = [(100, 40), (100, -40), (-100, 40),
                    (-100, -40)]  # board coordinates
    board_x = [coord[0] for coord in board_coords]
    board_y = [coord[1] for coord in board_coords]

    # Find possessions that start within range of boards
    board_possessions = []
    nonboard_possessions = []
    for possession in possessions:
        start_x, start_y = possession[0]['xadjcoord'], possession[0]['yadjcoord']
        if any(abs(start_x - x) <= board_range or abs(start_y - y) <= board_range for x, y in board_coords):
            board_possessions.append(possession)
        else:
            nonboard_possessions.append(possession)

    # Find possessions that start outside range of boards
    return board_possessions, nonboard_possessions

# boards, non_boards = separate_possessions_by_board(possessions)
# corsiDensity(possessions, (40,100))

a=0
# corsiDensity(possessions, (40, 40))
# plot_numShots(possessions)