'''
Purpose: Update safety scores based on time of day and season, and
    each morning pull recent data
'''
import time
import datetime
import pickle
import schedule
import generate_data
import get_pctiles
import crime_stat_map

def get_season(month):
    '''
    Purpose:
        Get season of current month
    Inputs:
        month: current month
    Returns:
        season (String): season of month
    '''
    seasons_months = {
        'winter': [12, 1, 2],
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'fall': [9, 10, 11]}
    for season in seasons_months:
        for months in season:
            if month == months:
                return season
    return 'Invalid month'


def morning_update():
    '''
    Pull recent data, update safety scores
    based on time of day and season
    '''
    print('It is 01:00! Starting morning update')
    month = datetime.datetime.now().month
    season = get_season(month)
    generate_data.gen_data(recent=True, safety_scores=('morning', season))
    time_now = str(datetime.datetime.now()).split(' ')[1]
    print('Morning update complete. Current time: ' + time_now)


def night_update():
    '''
    Update safety scores based on time of day
    and season
    '''
    print('It is 09:00! Starting night update')
    month = datetime.datetime.now().month
    season = get_season(month)
    generate_data.gen_data(safety_scores=('night', season))
    time_now = str(datetime.datetime.now()).split(' ')[1]
    print('Night update complete. Current time: ' + time_now)


def weekly_update():
    '''
    Update crime score percentiles and Folium community
    area plots weekly
    '''
    print("It is 04:00 on Monday! Starting weekly update")
    #Update plots weekly
    generate_data.gen_data(plot=True)
    #Update percentiles weekly
    pctiles, max_nodes = get_pctiles.get_pctiles(plot=True)
    pickle.dump(pctiles, open("safechicago/pickle_files/pctiles.p", "wb"))
    pickle.dump(max_nodes, open("safechicago/pickle_files/max_nodes.p", "wb"))
    #Update crime stat map weekly
    crime_stat_map.generate_map(max_nodes)
    time_now = str(datetime.datetime.now()).split(' ')[1]
    print('Weekly update complete. Current time: ' + time_now)


schedule.every().day.at('01:00').do(morning_update)
schedule.every().day.at('09:00').do(night_update)
schedule.every().monday.at('04:00').do(weekly_update)

while True:
    schedule.run_pending()
    time.sleep(60) # Wait one minute

#To run: nohup python3 daily_update.py &
