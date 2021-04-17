'''
Purpose:
    Calculate optimal route using Dijkstra's algorithm by adjusting street
    lengths and output route to a Folium map. It is different from
    dikstra_com.py because it is not bounded by the community area.
'''
import pickle
from math import radians, cos, sin, asin, sqrt
import osmnx as ox
import numpy as np
import directions
import google_maps
from dijkstra_com import get_nodes, get_temp, create_map


def get_route(threshold, curr_loc, destination):
    '''
    Purpose:
        Get direction from curr_loc to destination given threshold of
        safety level.
    Inputs:
        threshold (string): user inputs. 'default', 'safer', 'safest'
        curr_loc (string): user inputs. (Ex) "1100 E 57th St, Chicago,
            IL 60637" (example)
        destination (string): user inputs. (Ex) "1121 E 60th St, Chicago,
            IL 60637" (example)
    Outputs:
        direction (list): list of directions from curr_loc to destination
    Note:
        Saves folium map with route from curr_loc to destination. This
        folium map will be called to our website.
    '''
    curr = google_maps.get_lat_lng(curr_loc + ', Chicago')
    dest = google_maps.get_lat_lng(destination + ', Chicago')

    lat1, lng1 = curr
    lat2, lng2 = dest
    dist_factor = 1.2
    distance = dist_factor * haversine(lng1, lat1, lng2, lat2)

    lats = [lat1, lat2]
    lngs = [lng1, lng2]
    center = find_center_point(lats, lngs)

    center = find_center_point((curr[0], dest[0]), (curr[1], dest[1]))
    print('Center found')
    G = ox.core.graph_from_point(center, distance=distance)
    print('G downloaded')
    nodes_df, street_df = ox.graph_to_gdfs(G, nodes=True, edges=True)
    print('G converted to nodes, streets')
    safety_score_coms = combine_safety_scores()
    print('Safety scores combined')

    orig_node, target_node = get_location(curr, dest, G)

    temp = get_temp(curr)

    if threshold == 'safest':
        safest_nodes, safer_nodes, unsafe_nodes = get_nodes(safety_score_coms,\
            ['safest', 'safer', 'unsafe'], temp)

        low_nodes = street_df['u'].isin(safest_nodes) | street_df['v']\
            .isin(safest_nodes)
        street_df.loc[low_nodes, 'length'] *= 10

        med_nodes = street_df['u'].isin(safer_nodes) | street_df['v']\
            .isin(safer_nodes)
        street_df.loc[med_nodes, 'length'] *= 2

        high_nodes = street_df['u'].isin(unsafe_nodes) | street_df['v']\
            .isin(unsafe_nodes)
        street_df.loc[high_nodes, 'length'] *= 2
        print("Nodes list created")

    elif threshold == 'safer':
        safer_nodes, unsafe_nodes = get_nodes(safety_score_coms,\
            ['safer', 'unsafe'], temp)

        med_nodes = street_df['u'].isin(safer_nodes) | street_df['v']\
            .isin(safer_nodes)
        street_df.loc[med_nodes, 'length'] *= 10

        high_nodes = street_df['u'].isin(unsafe_nodes) | street_df['v']\
            .isin(unsafe_nodes)
        street_df.loc[high_nodes, 'length'] *= 2
        print("Nodes list created")

    G_adj, route = create_map(curr_loc, destination, nodes_df, street_df,\
        curr, dest, orig_node, target_node, G)
    direction = directions.get_directions(G_adj, route)

    return direction


def haversine(lon1, lat1, lon2, lat2):
    # Following code comes from PA3.
    '''
    Calculate the circle distance between two points
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return m


def find_center_point(lats, lngs):
    '''
    Purpose:
        Find center point between current location and destination
    Inputs:
        lats (list): list of 2 latitudes
        lngs (list): list of 2 longitudes
    Returns:
        newX, newY (tuple): latitude, longitude for center point
    '''
    # Source: https://stackoverflow.com/questions/
    # 6671183/calculate-the-center-point-of-multiple-
    # latitude-longitude-coordinate-pairs/14231286
    X = 0.0
    Y = 0.0
    Z = 0.0

    for i in range(2):
        lat = lats[i] * np.pi / 180
        lng = lngs[i] * np.pi / 180

        a = np.cos(lat) * np.cos(lng)
        b = np.cos(lat) * np.sin(lng)
        c = np.sin(lat)

        X += a
        Y += b
        Z += c

    X /= 2
    Y /= 2
    Z /= 2

    lng = np.arctan2(Y, X)
    hyp = np.sqrt(X * X + Y * Y)
    lat = np.arctan2(Z, hyp)

    newX = (lat * 180 / np.pi)
    newY = (lng * 180 / np.pi)
    return newX, newY


def import_data():
    '''
    Purpose:
        Generate dictionary of community areas linked to community area
        numbers
    Inputs:
        Nothing
    Returns:
        community_areas (dictionary): dictionary linking community area
            names to community area numbers
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

    return community_areas


def get_location(curr, dest, G):
    '''
    Purpose:
        Gets the nearest node of current and destination location. We use
        Google Maps API to find the locations in latitude and longitude format.
    Inputs:
        community:
        curr: current location lat/lng
        dest: destination lat/lng
        G: geodataframe of community area
    Outputs:
        orig_node (integer): node_id of nearest node to destination
        target_node (integer): node_id of nearest node to destination
    '''
    orig_node = ox.get_nearest_node(G, curr, method='euclidean')
    target_node = ox.get_nearest_node(G, dest, method='euclidean')
    return orig_node, target_node


def combine_safety_scores():
    '''
    Purpose:
        Combine safety score dictionaries for all community areas
    Inputs:
        Nothing
    Returns:
        safety_score_coms (dict): dictionary linking all nodes for all
            community areas to safety scores
    '''
    community_areas = import_data()
    safety_score_coms = {}
    for community in community_areas:
        com_cleaned = community.replace(" ", "_")
        safety_filename = "pickle_files/safety_files/safety_score_com_" + com_cleaned + ".p"
        safety_score_com = pickle.load(open(safety_filename, "rb"))
        safety_score_coms.update(safety_score_com)
    return safety_score_coms
