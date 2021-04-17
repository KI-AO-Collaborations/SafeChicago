'''
Purpose: Generate files used to construct safety_score_com_dict,
which is a dictionary that maps community areas to dictionary
of key as node_id and value as corresponding safety score.
'''
import pickle
import pandas as pd
import geopandas as gpd
import cleaned_dataset_crime
import community_boundaries
import recent_data
import safety_score


def gen_data(data=False, com_Gs=False, com_dict=False, plot=False,\
                recent=False, safety_scores=False):
    '''
    Purpose:
        Construct datafiles necessary to generate safety_score_com_dict
    Inputs:
        inputs that indicate whether to construct the dataframe or just
        call a pickle file already saved in disk.
    Outputs:
        data (Pandas DataFrame): crime data imported from Chicago Data Portal
        com_Gs (dictionary): maps community area to boundary geodataframe.
        com_dict (dictionary): maps community area to cleaned dataframe ready
            to be used to get safety scores.
        plot (boolean): if True, plot stats in cleaned_dataset_crime,
            otherwise don't plot
        safety_score_com_dict (dictionary): maps community areas to
            dictionary of key as node_id and value as corresponding
            safety score.
    Note:
        We always keep com_Gs = False to avoid unnecessary computations.
        com_Gs is a dictionary that maps community areas to its boundary
        geodataframe. Thus, it does not change over time.
    '''
    ### Construction of data
    if safety_scores and not com_dict: # Must load com_dict in order to call
                                       # safety_score.get_safety_score_com_dict
        com_dict = True
    if plot and not com_dict: # Plotting done in cleaned_dataset_crime, which
                              # is only called if com_dict=True
        com_dict = True
    if com_dict and not data: # Must load data in order to load com_dict
        data = 'load'
    if data:
        if data == 'new':
            data = gen_data_from_csv('data/crime_data_2017.csv')
            pickle.dump(data, open('safechicago/pickle_files/data.p', 'wb'))
        elif data == 'load':
            data = pickle.load(open('safechicago/pickle_files/data.p', 'rb'))
    community_areas, chicago_boundaries = import_data()
    print('Data import successful')

    ### Construction of com_Gs
    if com_Gs == 'by_com': # Create com_G files for each community area
        com_Gs = community_boundaries.get_Gs(chicago_boundaries,\
            community_areas)
        for com, com_G in com_Gs.items():
            com_cleaned = com.replace(' ', '_')
            filename = 'safechicago/pickle_files/com_G_files/com_G_' +\
                com_cleaned + '.p'
            pickle.dump(com_G, open(filename, 'wb'))
        print('Com Gs generated')
    elif com_Gs == 'all': # Create com_G file containing all community areas
        com_Gs = community_boundaries.get_Gs(chicago_boundaries,\
            community_areas)
        pickle.dump(com_Gs, open('safechicago/pickle_files/com_Gs.p', 'wb'))
    else:
        com_Gs = pickle.load(open('safechicago/pickle_files/com_Gs.p', 'rb'))
        print('Com Gs loaded')

    ### Construction of com_dict
    if com_dict:
        com_dict = cleaned_dataset_crime.get_com_dict(data, com_Gs,\
            community_areas, plot)
        pickle.dump(com_dict, open('safechicago/pickle_files/com_dict.p',\
            'wb'))
        print('Com dict generated')
    else:
        com_dict = pickle.load(open('safechicago/pickle_files/com_dict.p',\
            'rb'))
        print('Com dict loaded')
    if recent:
        com_dict = recent_data.gen_recent_data(com_Gs, community_areas,\
            com_dict)
        pickle.dump(com_dict, open('safechicago/pickle_files/com_dict.p',\
            'wb'))
        print('Com dict updated')

    ### Construction of safety_score_com_dict
    if safety_scores:
        time_of_day, season = safety_scores # safety_scores is a tuple of
                                            # time_of_day, season
        safety_score_com_dict = safety_score.get_safety_score_com_dict(\
            com_dict, time_of_day, season)
        print('Safety scores calculated')
        for com, safety_score_com in safety_score_com_dict.items():
            com_cleaned = com.replace(' ', '_')
            filename = 'safechicago/pickle_files/safety_files/' +\
                'safety_score_com_' + com_cleaned + '.p'
            pickle.dump(safety_score_com, open(filename, 'wb'))


def import_data():
    '''
    Purpose:
        Generate dictionary of community areas linked to community area
        numbers, and community area polygon boundaries
    Inputs:
        Nothing
    Returns:
        community_areas (dictionary): dictionary linking community area
            names to community area numbers
        chicago_boundaries (GeoDataFrame): data on community area boundaries
    '''
    community_areas =\
        {'ROGERS PARK': 1, 'WEST RIDGE': 2, 'UPTOWN': 3,
         'LINCOLN SQUARE': 4, 'NORTH CENTER': 5, 'LAKE VIEW': 6,
         'LINCOLN PARK': 7, 'NEAR NORTH SIDE': 8, 'EDISON PARK': 9,
         'NORWOOD PARK': 10, 'JEFFERSON PARK': 11, 'FOREST GLEN': 12,
         'NORTH PARK': 13, 'ALBANY PARK': 14, 'PORTAGE PARK': 15,
         'IRVING PARK': 16, 'DUNNING': 17, 'MONTCLARE': 18,
         'BELMONT CRAGIN': 19, 'HERMOSA': 20, 'AVONDALE': 21,
         'LOGAN SQUARE': 22, 'HUMBOLDT PARK': 23, 'WEST TOWN': 24,
         'AUSTIN': 25, 'WEST GARFIELD PARK': 26, 'EAST GARFIELD PARK': 27,
         'NEAR WEST SIDE': 28, 'NORTH LAWNDALE': 29, 'SOUTH LAWNDALE': 30,
         'LOWER WEST SIDE': 31, 'LOOP': 32, 'NEAR SOUTH SIDE': 33,
         'ARMOUR SQUARE': 34, 'DOUGLAS': 35, 'OAKLAND': 36, 'FULLER PARK': 37,
         'GRAND BOULEVARD': 38, 'KENWOOD': 39, 'WASHINGTON PARK': 40,
         'HYDE PARK': 41, 'WOODLAWN': 42, 'SOUTH SHORE': 43, 'CHATHAM': 44,
         'AVALON PARK': 45, 'SOUTH CHICAGO': 46, 'BURNSIDE': 47,
         'CALUMET HEIGHTS': 48, 'ROSELAND': 49, 'PULLMAN': 50,
         'SOUTH DEERING': 51, 'EAST SIDE': 52, 'WEST PULLMAN': 53,
         'RIVERDALE': 54, 'HEGEWISCH': 55, 'GARFIELD RIDGE': 56,
         'ARCHER HEIGHTS': 57, 'BRIGHTON PARK': 58, 'MCKINLEY PARK': 59,
         'BRIDGEPORT': 60, 'NEW CITY': 61, 'WEST ELSDON': 62, 'GAGE PARK': 63,
         'CLEARING': 64, 'WEST LAWN': 65, 'CHICAGO LAWN': 66,
         'WEST ENGLEWOOD': 67, 'ENGLEWOOD': 68, 'GREATER GRAND CROSSING': 69,
         'ASHBURN': 70, 'AUBURN GRESHAM': 71, 'BEVERLY': 72,
         'WASHINGTON HEIGHTS': 73, 'MOUNT GREENWOOD': 74, 'MORGAN PARK': 75,
         'OHARE': 76, 'EDGEWATER': 77}

    chicago_boundaries = gpd.read_file('data/boundaries.geojson')

    return community_areas, chicago_boundaries


def gen_data_from_csv(filename):
    '''
    Purpose:
        Generate historical crime data from CSV and clean the file
    Inputs:
        filename: filename of CSV
    Returns:
        (DataFrame): cleaned historical crime data
    '''
    cols = ['ID', 'Date', 'Primary Type', 'Community Area', 'Latitude',\
        'Longitude']
    data = pd.read_csv(filename, usecols=cols, parse_dates=['Date'],\
        infer_datetime_format=True)
    data.columns = [column.lower().replace(' ', '_')\
        for column in data.columns]
    data.dropna(inplace=True)
    data.set_index('id', inplace=True)
    data['primary_type'] = data['primary_type'].astype('category')
    return data
