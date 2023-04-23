import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Linhac_df_keyed_20_games.csv')
#get rows where possession changes occur, returns boolean array


def possession_changes(data):
    data['prev_possession'] = data['currentpossession'].shift()

    data['possession_change'] = (
        data['prev_possession'] == data['currentpossession']-1)
    if data['possession_change'].isna().any():
        data['possession_change'] = data['currentpossession']
    return data['possession_change'] == 1


def group_possessions(data):
    possession_change = possession_changes(data)
    #split the data into possessions
    #store each possession as a dataframe in a list

    possessions = []
    current_possession = []
    for index, row in data.iterrows():
        if possession_change[index]:
            possessions.append(current_possession)
            current_possession = []
        current_possession.append(row)
    return possessions
        


a=0
