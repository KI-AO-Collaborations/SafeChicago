'''
Purpose:
    Clean crime dataframe with nearest node information for each
    community area.
'''
import numpy as np
import pandas as pd
import osmnx as ox
from matplotlib import pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'


def get_com_dict(data, com_Gs, community_areas, plot=False):
    '''
    Purpose:
        Construct crime dataframe for each community area. We
        cleaned dataframe to have additional information such
        as nearest node, hour, month, time of day, season. Can
        also generate plots for relevant information for each
        community area.
    Inputs:
        data (Pandas DataFrame): crime data imported from Chicago Data Portal
        com_Gs (dictionary): maps community area to boundary geodataframe.
        community_areas (dictionary): maps community area to community
            code number
        plot (boolean): if True, plot stats, otherwise don't plot
    Outputs:
        com_df (dictionary): creates a dictionary with key as community area
            with crime dataframe
        (ex) com_df = {'HYDE PARK': hyde_park_df, 'DOUGLAS': douglas_df, etc.}
    '''
    com_dict = {}
    seasons_months = {
        'winter': [12, 1, 2],
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'fall': [9, 10, 11]}
    time_of_day_hours = {
        'morning': [1, 2, 3, 4, 5, 6, 7, 8],
        'night': [0, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,\
            20, 21, 22, 23]}

    for com in community_areas:
        # specific community crimes
        com_crime = data[data['community_area'] == community_areas[com]]
        G = com_Gs[com]
        # Finds the nearest node id:
        com_crime['nearest_node'] = ox.get_nearest_nodes(G,\
            np.array(com_crime['longitude']), np.array(\
                com_crime['latitude']), method='kdtree')
        com_crime.drop(columns=['latitude', 'longitude'], inplace=True)
        com_crime['hour'] = com_crime['date'].dt.hour
        com_crime['month'] = com_crime['date'].dt.month
        com_crime['time_of_day'] = np.nan #Fill in values as NaN
        com_crime['season'] = np.nan #Fill in values as NaN

        # Following lines of code motivated by:
        # https://stackoverflow.com/questions/16327055/how-to-add-
        # an-empty-column-to-a-dataframe
        for time_of_day, hours in time_of_day_hours.items():
            com_crime.loc[com_crime['hour'].\
            isin(hours), 'time_of_day'] = time_of_day
        for season, months in seasons_months.items():
            com_crime.loc[com_crime['month'].\
            isin(months), 'season'] = season

        if plot:
            graph_by_time(com_crime, com)
            graph_by_month(com_crime, com)
            graph_by_season(com_crime, com)
        else:
            com_crime = com_crime.drop(columns=['hour', 'month'])
            # If plotting, need these columns to make graphs for
            # entirety of Chicago

        com_dict[com] = com_crime

    if plot: # Generate graphs for entirety of Chicago
        com_df_merged = pd.concat([com for com in com_dict.values()], axis=0)
        graph_by_time(com_df_merged, 'CHICAGO')
        graph_by_month(com_df_merged, 'CHICAGO')
        graph_by_season(com_df_merged, 'CHICAGO')
        for com, com_crime in com_dict.items():
            com_dict[com] = com_crime.drop(columns=['hour', 'month'])

    return com_dict


def graph_by_time(com_crime_df, com_area):
    '''
    Constructs crime frequency over different hours
    '''
    vals = com_crime_df['hour'].value_counts()
    plt.bar(x=vals.index, height=vals)
    plt.xlabel('Time of Day (Hour)')
    plt.ylabel('Total Number of Crimes')
    plt.title('Crime Counts by Time of Day for ' + com_area.title())
    filename = 'data/folium_figures/' + com_area.replace(' ', '_') + '_time.png'
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()


def graph_by_month(com_crime_df, com_area):
    '''
    Constructs crime frequency over different months
    '''
    vals = com_crime_df['month'].value_counts()
    plt.bar(x=vals.index, height=vals)
    plt.xlabel('Month')
    plt.ylabel('Total Number of Crimes')
    plt.title('Crime Counts by Month for ' + com_area.title())
    filename = 'data/folium_figures/' + com_area.replace(' ', '_') + '_month.png'
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()


def graph_by_season(com_crime_df, com_area):
    '''
    Constructs crime frequency over different seasons
    '''
    vals = com_crime_df['season'].value_counts()
    plt.bar(x=vals.index, height=vals)
    plt.xlabel('Season')
    plt.ylabel('Total Number of Crimes')
    plt.title('Crime Counts by Season for ' + com_area.title())
    filename = 'data/folium_figures/' + com_area.replace(' ', '_') + '_season.png'
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()
