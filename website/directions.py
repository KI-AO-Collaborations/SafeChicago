'''
Purpose: Gets direction from current location to destination location
    using Google Maps Directions API.
'''
import re
import googlemaps


def get_directions(G, route):
    '''
    Purpose:
        Gets list of directions given route or list of nodes to go through.
    Inputs:
        G (GeoDataFrame): data of community area
        route (list): list of nodes
    Outputs:
        directions (list): List of strings giving directions using route
            information given.
    '''
    steps = find_route(G, route)
    directions = []
    for step in steps:
        prev_dir = "prev"
        for leg in step[0]['legs']:
            direction = leg['steps'][0]['html_instructions']
            cleaned_dir = re.sub('<[^<]+?>', '', direction)
            split_phrase = cleaned_dir.split(" ")
            if split_phrase[-1] in ('left', 'right'):
                split_phrase = split_phrase[:-5]
                split_phrase[-1] = split_phrase[-1][:-11]
            cleaned_dir = " ".join(split_phrase)
            if len(split_phrase) > 1:
                min_len = min(len(cleaned_dir), len(prev_dir))
                if min_len != len(cleaned_dir) and\
                 cleaned_dir[:min_len] == prev_dir[:min_len]:
                    directions.append(cleaned_dir)
                    prev_dir = cleaned_dir
                elif min_len != len(prev_dir) and\
                 cleaned_dir[:min_len] == prev_dir[:min_len]:
                    pass
                elif cleaned_dir != prev_dir:
                    directions.append(cleaned_dir)
                    prev_dir = cleaned_dir

    return directions


def find_route(G, route):
    '''
    Purpose:
        Finds the steps dictionary information using Google Maps API.
    Inputs:
        G (GeoDataFrame): data of community area
        route (list): list of nodes
    Outputs:
        steps (dictionary): steps dictionary provided by Google Maps API.
    '''
    gmaps = googlemaps.Client(key='AIzaSyAmmm3Lc1n897ijWvvFuyg1TR-kixbAvAQ')
    way_point = []

    # Convert node into location data so that we can use Google Maps API
    # on these locations:
    for node_id in route:
        loc = {}
        loc['lat'] = G.node[node_id]['y']
        loc['lng'] = G.node[node_id]['x']
        way_point.append(loc)
    split_waypoints = new_route(way_point)
    steps = []
    for waypoint in split_waypoints:
        directions_result = gmaps.directions(waypoint[0], waypoint[-1],\
            waypoints=waypoint[1:-1], mode="walking")
        steps.append(directions_result)
    return steps


def new_route(way_point):
    '''
    Purpose:
        We can only request directions with 23 location points. So,
        we split our node location into groups of 23.
    Inputs:
        way_point (list): list of location data points.
    Outputs:
        way_point (list of lists): updated list containing groups of lists with
            less than 23 location points.
    '''
    if len(way_point) > 23:
        return [way_point[:23]] + new_route(way_point[23:])
    return [way_point]
