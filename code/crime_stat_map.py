'''
Purpose: Generate Folium map with crime statistics. Has the following
functions.
(1) selection feature that enables user to select crime statistics
between years 2017, 2018, 2019.
(2) Marker in each community area, which contains histogram of crime
statistics.
(3) Black circle, which represents the most dangerous intersection
within community area.
(4) Search bar that enables user to look at specific community area
once inputinng the community area name in the bar.
'''
import os
import pickle
import base64
import datetime
import folium
from folium.plugins import HeatMap, Search
import branca
import generate_data


def generate_map(nodes_list):
    '''
    Purpose: generate the folium map.
    Inputs:
        nodes_list (list): list of node data of node with the highest safety
        score in each community area. Node data stored as a tuple of
        (lat, lng, max_score).
    Outputs:
        Nothing. Saves 'Chicago map.html' that we use in our Django Website.
    '''
    crime_weights, com_lat_lng = import_data()

    #### Crime data
    data = pickle.load(open('safechicago/pickle_files/data.p', 'rb'))
    data['weights'] = data['primary_type'].replace(crime_weights)
    data['year'] = data['date'].dt.year

    #### Boundary data
    ### Generates marker with crime statistics histogram for each community area:
    community_areas, com_area_polygons = generate_data.import_data()

    #### Create Map
    m = folium.Map([41.8781, -87.6298], zoom_start=10, tiles='cartodbpositron')

    # Shows community area name when hover mouse over a community area.
    community_geo = folium.GeoJson(com_area_polygons, name='Community Areas',\
        tooltip=folium.GeoJsonTooltip(fields=['community'],\
        aliases=['Community:'], localize=True)).add_to(m)

    # Provides search bar:
    Search(layer=community_geo, geom_type='Polygon',\
        placeholder='Search for Chicago Community', collapsed=False,\
        search_label='community', weight=3).add_to(m)

    ## Heat Map
    dangerous_nodes = folium.FeatureGroup(name='Most Dangerous Intersections')
    histograms = folium.FeatureGroup(name='Histograms')

    feature_groups = [dangerous_nodes, histograms]
    year_of_recent_data = (datetime.datetime.now() -\
                            datetime.timedelta(days=9)).year
    for year in range(2017, year_of_recent_data + 1):
        feature_groups.append(folium.FeatureGroup(name='Crime ' + str(year)))
        data_year = data[data['year'] == year]
        data_year = data_year[['latitude', 'longitude', 'weights']].to_numpy()
        HeatMap(data_year, blur=5).add_to(feature_groups[len(feature_groups) - 1])

    for loc_info in nodes_list:
        lat, lng, score = loc_info
        for lat_val in lat:
            lat = lat_val
        for lng_val in lng:
            lng = lng_val
        folium.CircleMarker([lat, lng], radius=5, color='black',\
            fill_color='black', fill=True, popup=folium.Popup(\
            'Safety Score: ' + str(score))).add_to(feature_groups[0])

    for com in community_areas:
        lat, lng = com_lat_lng[com]
        inter_html = generate_html('_intersection_score.png', com)
        time_html = generate_html('_time.png', com)
        month_html = generate_html('_month.png', com)
        season_html = generate_html('_season.png', com)
        images_html = inter_html + time_html + month_html + season_html
        html = '<h1> ' + com.title() + ' </h1><br> ' +\
                '<body>' + images_html + '</body>'
        iframe = branca.element.IFrame(html=html, width=600, height=400)
        popup = folium.Popup(iframe, max_width=800)
        folium.Marker([lat, lng], popup=popup).add_to(feature_groups[1])

    for feature_group in feature_groups:
        m.add_child(feature_group)
    m.add_child(folium.LayerControl())

    m.save('safechicago/safe_route/static/Chicago map.html')

def generate_html(filename, com):
    '''
    Purpose:
        Generate HTML tags to open the images stored at
        img_filepath_beg + filename
    Inputs:
        filename: end of filepath
        com: community area
    Returns:
        html_ret (str): formatted HTML tags
    '''
    filepath = os.path.dirname(os.path.abspath(__file__))
    img_filepath_beg = filepath + '/safechicago/safe_route/static/' +\
            'folium_figures/' + com.replace(' ', '_')
    filepath = img_filepath_beg + filename
    encoded_file = base64.b64encode(open(filepath, 'rb').read())\
        .decode('utf8')
    create_html = ('<img src="data:image/png;base64,{}" width="500"' +\
            'height="300">').format
    html_ret = create_html(encoded_file)
    return html_ret

def import_data():
    '''
    Purpose:
        Get crime weights and latitude and longitutdes for community areas
    Inputs:
        Nothing
    Returns:
        crime_weights, com_lat_lng (tuple): crime weights and community
            area latitudes and longitudes
    '''
    crime_weights =\
                    {'THEFT': 1, 'BATTERY': 2, 'CRIMINAL DAMAGE': 0.5,
                     'ASSAULT': 2, 'DECEPTIVE PRACTICE': 0.1,
                     'OTHER OFFENSE': 0.1, 'NARCOTICS': 0.1, 'BURGLARY': 1,
                     'ROBBERY': 1, 'MOTOR VEHICLE THEFT': 0.1,
                     'CRIMINAL TRESPASS': 0.1, 'WEAPONS VIOLATION': 0.5,
                     'OFFENSE INVOLVING CHILDREN': 0.5,
                     'CRIM SEXUAL ASSAULT': 1, 'PUBLIC PEACE VIOLATION': 0.1,
                     'INTERFERENCE WITH PUBLIC OFFICER': 0.1,
                     'SEX OFFENSE': 0.1, 'PROSTITUTION': 0.1, 'HOMICIDE': 20,
                     'ARSON': 2, 'LIQUOR LAW VIOLATION': 0.5, 'STALKING': 0.5,
                     'GAMBLING': 0.1, 'KIDNAPPING': 10, 'INTIMIDATION': 0.5,
                     'CONCEALED CARRY LICENSE VIOLATION': 0.5, 'OBSCENITY': 0.5,
                     'NON-CRIMINAL': 0, 'HUMAN TRAFFICKING': 10,
                     'PUBLIC INDECENCY': 0.5, 'OTHER NARCOTIC VIOLATION': 0.1,
                     'NON-CRIMINAL (SUBJECT SPECIFIED)': 0}

    com_lat_lng =\
                {'ROGERS PARK': (42.0106, -87.6696), 'WEST RIDGE': (42.0006, -87.6926),
                 'UPTOWN': (41.98088, -87.65999), 'LINCOLN SQUARE': (41.9699, -87.6887),
                 'NORTH CENTER': (41.9509, -87.6828), 'LAKE VIEW': (41.9398, -87.6589),
                 'LINCOLN PARK': (41.9255, -87.6488), 'NEAR NORTH SIDE': (41.9039, -87.6315),
                 'EDISON PARK': (42.0054, -87.8133), 'NORWOOD PARK': (41.9856, -87.8069),
                 'JEFFERSON PARK': (41.9825, -87.7704), 'FOREST GLEN': (41.9792, -87.7514),
                 'NORTH PARK': (41.9843, -87.7260), 'ALBANY PARK': (41.9683, -87.7280),
                 'PORTAGE PARK': (41.9537, -87.7645), 'IRVING PARK': (41.9538, -87.7193),
                 'DUNNING': (41.9472, -87.8065), 'MONTCLARE': (41.9294, -87.7982),
                 'BELMONT CRAGIN': (41.9264, -87.7659), 'HERMOSA': (41.9215, -87.7344),
                 'AVONDALE': (41.9415, -87.7025), 'LOGAN SQUARE': (41.9231, -87.7093),
                 'HUMBOLDT PARK': (41.8991, -87.7213), 'WEST TOWN': (41.8936, -87.6722),
                 'AUSTIN': (41.8949, -87.7654), 'WEST GARFIELD PARK': (41.8806, -87.7292),
                 'EAST GARFIELD PARK': (41.8810, -87.7012), 'NEAR WEST SIDE': (41.8811, -87.6630),
                 'NORTH LAWNDALE': (41.8585, -87.7139), 'SOUTH LAWNDALE': (41.8458, -87.7058),
                 'LOWER WEST SIDE': (41.8523, -87.6660), 'LOOP': (41.8786, -87.6251),
                 'NEAR SOUTH SIDE': (41.8608, -87.6257), 'ARMOUR SQUARE': (41.8408, -87.6340),
                 'DOUGLAS': (41.8347, -87.6180), 'OAKLAND': (41.8227, -87.6014),
                 'FULLER PARK': (41.8091, -87.6334), 'GRAND BOULEVARD': (41.8131, -87.6178),
                 'KENWOOD': (41.8095, -87.5933), 'WASHINGTON PARK': (41.7945, -87.6160),
                 'HYDE PARK': (41.7948, -87.5917),
                 'WOODLAWN': (41.7806, -87.5915), 'SOUTH SHORE': (41.7600, -87.5742),
                 'CHATHAM': (41.7401, -87.6146), 'AVALON PARK': (41.7442, -87.5856),
                 'SOUTH CHICAGO': (41.7397, -87.5544), 'BURNSIDE': (41.7281, -87.5964),
                 'CALUMET HEIGHTS': (41.7298, -87.5705), 'ROSELAND': (41.7108, -87.6236),
                 'PULLMAN': (41.6895, -87.6061), 'SOUTH DEERING': (41.6737, -87.5753),
                 'EAST SIDE': (41.7080, -87.5352), 'WEST PULLMAN': (41.6716, -87.6333),
                 'RIVERDALE': (41.6611, -87.6038), 'HEGEWISCH': (41.6555, -87.5459),
                 'GARFIELD RIDGE': (41.7941, -87.7706), 'ARCHER HEIGHTS': (41.8079, -87.7236),
                 'BRIGHTON PARK': (41.8194, -87.6990), 'MCKINLEY PARK': (41.8316, -87.6729),
                 'BRIDGEPORT': (41.8364, -87.6487), 'NEW CITY': (41.8067, -87.6680),
                 'WEST ELSDON': (41.7929, -87.7222), 'GAGE PARK': (41.7954, -87.6962),
                 'CLEARING': (41.7784, -87.7692), 'WEST LAWN': (41.7728, -87.7223),
                 'CHICAGO LAWN': (41.7719, -87.6954), 'WEST ENGLEWOOD': (41.7781, -87.6667),
                 'ENGLEWOOD': (41.7753, -87.6416), 'GREATER GRAND CROSSING': (41.7657, -87.6153),
                 'ASHBURN': (41.7479, -87.7072), 'AUBURN GRESHAM': (41.7434, -87.6562),
                 'BEVERLY': (41.7171, -87.6762), 'WASHINGTON HEIGHTS': (41.7176, -87.6431),
                 'MOUNT GREENWOOD': (41.6931, -87.7124), 'MORGAN PARK': (41.6878, -87.6690),
                 'OHARE': (41.9773, -87.8369), 'EDGEWATER': (41.9872, -87.6612)}
    return crime_weights, com_lat_lng
