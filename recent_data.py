'''
Purpose:
    Pull recent data from Chicago Data Portal,
    append it to com_dict
'''
import datetime
import pandas as pd
from sodapy import Socrata
import cleaned_dataset_crime

def get_day(days_ago):
    '''
    Purpose:
        Get datetime object of day that is days_ago days
        ago. Convert to String so can be appended to
        String input.
    Inputs:
        days_ago: how many days ago the day should be
    Returns:
        past_date (str): day that is days_ago days ago
    '''
    date_with_time = datetime.datetime.now() - datetime\
        .timedelta(days=days_ago)
    past_date = str(date_with_time).split(' ')[0]
    return past_date


def import_recent_data(period=1):
    '''
    Purpose:
        Import and clean recent data from Chicago Data Portal
        using sodapy
    Inputs:
        period: how many days ago to pull data - adds 8 by default
        because the most recent data on Chicago Data portal is from
        1 week ago
    Returns:
        data (DataFrame): cleaned recent crime data pulled from Chicago
            Data Portal
    '''
    period += 8
    # Add 8 because the most recent data on Chicago Data Portal is from
    # 1 week ago
    token = 'MpJu4jCS2lTzwujnKo3uI0NCL'
    client = Socrata('data.cityofchicago.org', token)
    day = get_day(period)
    results = client.get('6zsd-86xi', select='community_area, date, id, '\
        'latitude, longitude, primary_type', where="date > '" + day + "'",\
        limit=5000000)
    data = pd.DataFrame.from_records(results)
    data['community_area'] = data['community_area'].astype(int)
    data[['latitude', 'longitude']] = data[['latitude', 'longitude']]\
        .astype(float)
    data['date'] = pd.to_datetime(data['date'].tolist())
    data['primary_type'] = data['primary_type'].astype('category')
    data.dropna(inplace=True)
    data.set_index('id', inplace=True)
    return data


def gen_recent_data(com_Gs, community_areas, com_dict_old):
    '''
    Purpose:
        Update com_dict to include most recent crime data
        pulled from Chicago Data Portal
    Inputs:
        com_Gs (dictionary): maps community area to boundary
            geodataframe.
        community_areas (dictionary): dictionary linking community area
            names to community area numbers
        com_dict_old (dictionary): maps community area to
            cleaned dataframe ready to be used to get safety scores.
    Returns:
        com_dict_new: updated com_dict that includes recent
            crime data
    '''
    daily_data = import_recent_data(period=1)

    com_dict_daily = cleaned_dataset_crime.get_com_dict(daily_data, com_Gs,\
        community_areas)
    com_dict_new = {}
    for com in community_areas:
        com_old = com_dict_old[com]
        com_daily = com_dict_daily[com]
        com_new = pd.concat([com_old, com_daily], sort=True)
        com_new.drop_duplicates(inplace=True)
        com_dict_new[com] = com_new
    return com_dict_new
