import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Linhac_df_keyed_20_games.csv')

lpr = data[data['eventname'] == 'lpr']
xcoords = lpr['xadjcoord']
ycoords = lpr['yadjcoord']
plt.plot(xcoords, ycoords)
a=0
