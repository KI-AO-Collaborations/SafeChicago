'''
Purpose:
    Create a dictionary that connects each community area with a dictionary of keys as nodes
    and values as safety score (get_safety_score_com_dict).
'''
import datetime
import numpy as np


def get_crime_weights():
    '''
    Purpose:
        Get crime weights
    Inputs:
        None
    Returns:
        crime_weights (dict): map crimes to crime weights
    '''
    crime_weights = {'THEFT': 1, 'BATTERY': 2, 'CRIMINAL DAMAGE': 0.5, 'ASSAULT': 2,\
        'DECEPTIVE PRACTICE': 0.1, 'OTHER OFFENSE': 0.1, 'NARCOTICS': 0.1,\
        'BURGLARY': 1, 'ROBBERY': 1, 'MOTOR VEHICLE THEFT': 0.1,\
        'CRIMINAL TRESPASS': 0.1, 'WEAPONS VIOLATION': 0.5,\
        'OFFENSE INVOLVING CHILDREN': 0.5, 'CRIM SEXUAL ASSAULT': 1,\
        'PUBLIC PEACE VIOLATION': 0.1, 'INTERFERENCE WITH PUBLIC OFFICER': 0.1,\
        'SEX OFFENSE': 0.1, 'PROSTITUTION': 0.1, 'HOMICIDE': 20, 'ARSON': 2,\
        'LIQUOR LAW VIOLATION': 0.5, 'STALKING': 0.5, 'GAMBLING': 0.1, 'KIDNAPPING': 10,\
        'INTIMIDATION': 0.5, 'CONCEALED CARRY LICENSE VIOLATION': 0.5,\
        'OBSCENITY': 0.5, 'NON-CRIMINAL': 0, 'HUMAN TRAFFICKING': 10,\
        'PUBLIC INDECENCY': 0.5, 'OTHER NARCOTIC VIOLATION': 0.1,\
        'NON-CRIMINAL (SUBJECT SPECIFIED)': 0}
    return crime_weights


def get_safety_score_com_dict(com_dict, current_time_of_day, current_season):
    '''
    Purpose: Create a dictionary that connects each community area with
        a dictionary with keys as nodes and value as safety score.
    Inputs:
        com_dict (dictionary): maps community area to cleaned dataframe
            ready to be used to get safety scores.
        current_time_of_day(string): 'morning' or 'night'
        current_season (string): 'winter , 'spring',  'summer', 'fall'
    Outputs:
        safety_score_com (dictionary): for each community area key, we have
            a value of dictionary which maps node_id to its corresponding
            safety score. (Ex) 'HYDE PARK': {100011: 10, 100100182: 0.003}
    '''
    current_date = datetime.datetime.now()
    crime_weights = get_crime_weights()
    counts_cols = ['season', 'time_of_day']
    counts_cols_today = [current_season, current_time_of_day]

    safety_score_com = {}
    for com_name, com_df in com_dict.items():
        com_df.drop('community_area', axis=1, inplace=True)
        com_df['primary_type'] = com_df['primary_type'].replace(crime_weights)
        update_table(zip(counts_cols, counts_cols_today), com_df)

        decay_weight = 0.998
        com_df['date'] = (current_date - com_df['date']).dt.days
        com_df['score'] = (com_df.loc[:, 'primary_type'] *\
            com_df.loc[:, 'season'] *\
            com_df.loc[:, 'time_of_day']) *\
            (decay_weight ** com_df['date'])

        safety_score = com_df.groupby('nearest_node')['score'].sum().to_dict()
        safety_score_com[com_name] = safety_score

    return safety_score_com


### HELPER FUNCTIONS:
def update_table(cols, com_df):
    '''
    Purpose:
        Update table so categorical variables are converted
        to values based on the current status of those
        variables today. If the status is the same, set it to be
        one, otherwise set it to be 1/2 so it is weighted
        less.
    Inputs:
        cols: list of tuples, first entry is column name
                to look at, second is the value of that
                column today
        com_df: community area crime dataframe
    Returns:
        Nothing
    '''
    for col in cols:
        col_name = col[0]
        col_today = col[1]
        com_df_scaled = np.ones(com_df.shape[0])
        com_df_scaled[np.array(com_df[col_name]) != (col_today)] /= 5
        #Divide for invalid time periods by 5
        com_df[col_name] = com_df_scaled
