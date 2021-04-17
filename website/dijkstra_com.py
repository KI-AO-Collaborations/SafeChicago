'''
Purpose:
    Calculate optimal route using Dijkstra's algorithm by adjusting street lengths
    and output route to a Folium map. It is different from dijkstra_nocom.py
    because it requires a community area boundary. In other words, the current
    and destination locations have to be in the same community area.
'''
import pickle
import osmnx as ox
import networkx as nx
import folium
from IPython.display import IFrame
import pyowm
import directions
import google_maps


def get_route(community, threshold, curr_loc, destination):
    '''
    Purpose:
        Get direction from curr_loc to destination given threshold
        of safety level.
    Inputs:
        community (string): user inputs. (Ex) 'HYDE PARK' etc.
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
    nodes_df, street_df, safety_score_com, G = load_data(community)

    curr, dest, orig_node, target_node = get_location(community, curr_loc,\
        destination, G)

    temp = get_temp(curr)

    if threshold == 'safest':
        safest_nodes, safer_nodes, unsafe_nodes = get_nodes(safety_score_com,\
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
        safer_nodes, unsafe_nodes = get_nodes(safety_score_com,\
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


def load_data(community):
    '''
    Purpose:
        Load G file from Pickle, turn it into a geodataframe and extract
        nodes_df and street_df, and load safety score dictionary by
        community area
    Inputs:
        community: community area
    Returns:
        nodes_df: geodataframe of nodes
        street_df: geodataframe of streets
        safety_score_com: dictionary linking community areas to safety scores
        G: geodataframe of community area
    '''
    com_cleaned = community.replace(" ", "_")
    G_filename = "pickle_files/com_G_files/com_G_" + com_cleaned + ".p"
    G = pickle.load(open(G_filename, "rb"))
    print("Com G loaded")
    nodes_df, street_df = ox.graph_to_gdfs(G, nodes=True, edges=True)

    safety_filename = "pickle_files/safety_files/safety_score_com_" +\
        com_cleaned + ".p"
    safety_score_com = pickle.load(open(safety_filename, "rb"))
    print("Safety scores loaded")
    return nodes_df, street_df, safety_score_com, G


def get_temp(curr):
    '''
    Purpose:
        Get whether the temperature at the current location
        is < 20 or > 95 degrees Fahrenheit (extreme weather)
    Inputs:
        curr: tuple of latitude, longitude of current location
    Returns:
        extreme_temp (boolean): True if temp < 20 or temp > 95,
            False otherwise
    '''
    lat, lng = curr
    key = '9b320be0b5b98b46bab63e4cf2464c0b'
    owm = pyowm.OWM(key)
    observation = owm.weather_at_coords(lat, lng)
    w = observation.get_weather()
    temp = w.get_temperature('fahrenheit')['temp']
    print("Current temperature pulled: ", temp)
    extreme_temp = temp < 20 or temp > 95
    return extreme_temp


def get_location(community, curr_loc, destination, G):
    '''
    Purpose:
        Gets the nearest node of current and destination location. We use
        Google Maps API to find the locations in latitude and
        longitude format.
    Inputs:
        community:
        curr_loc (string): name of the current location
        destination (string): name of the destination location
        G: geodataframe of community area
    Outputs:
        curr: current location lat/lng
        dest: destination lat/lng
        orig_node (integer): node_id of nearest node to destination
        target_node (integer): node_id of nearest node to destination
    '''
    curr = google_maps.get_lat_lng(curr_loc + " " + community +\
        ", Chicago")
    dest = google_maps.get_lat_lng(destination + " " + community +\
        ", Chicago")
    orig_node = ox.get_nearest_node(G, curr, method='euclidean')
    target_node = ox.get_nearest_node(G, dest, method='euclidean')
    return curr, dest, orig_node, target_node


def get_nodes(safety_score_com, node_selections, temp):
    '''
    Purpose:
        Get lists of nodes that should be adjusted for each safety rating
    Inputs:
        safety_score_com: dictionary linking community areas to safety scores
        node_selections: list of safety ratings, which node selections to
            adjust lengths
        temp: boolean of whether temperature is currently extreme
    Outputs:
        nodes_list: list of nodes that should be adjusted for each
            safety rating
    '''
    try:
        pctiles = pickle.load(open("pctiles.p", "rb"))
        safest, safer, unsafe = pctiles[:3]
        print("Percentiles extracted from pickle file")
    except:
        safest = 0.3310188654580943  # 25th percentile of safety scores
        safer = 0.9482861663702485  # 75th percentile of safety scores
        unsafe = 2.533931676614649  # 90th percentile of safety scores
        print("Percentiles pickle does not exist. Default percentiles used")
    if temp:
        nodes = {'safest': [node for node in safety_score_com if\
                     safety_score_com[node] * 0.75 >= safest],\
                 'safer': [node for node in safety_score_com if\
                     safety_score_com[node] * 0.75 >= safer],\
                 'unsafe': [node for node in safety_score_com if\
                     safety_score_com[node] * 0.75 >= unsafe]}
    else:
        nodes = {'safest': [node for node in safety_score_com if\
                     safety_score_com[node] >= safest],\
                 'safer': [node for node in safety_score_com if\
                     safety_score_com[node] >= safer],\
                 'unsafe': [node for node in safety_score_com if\
                     safety_score_com[node] >= unsafe]}
    nodes_list = [nodes[node_list] for node_list in node_selections]
    return nodes_list


def create_map(curr_loc, destination, nodes_df, street_df, curr, dest, orig_node, target_node, G):
    '''
    Purpose:
        Get optimized route and create Folium map based on it
    Inputs:
        curr_loc: name of current location
        destination: name of destination
        nodes_df: geodataframe of nodes
        street_df: geodataframe of streets
        curr: current location lat/lng
        dest: destination lat/lng
        orig_node (integer): node_id of nearest node to destination
        target_node (integer): node_id of nearest node to destination
        G: geodataframe
    Returns:
        G_adj: geodataframe with adjusted street lengths
        route: optimized route based on adjusted street lengths
    '''
    G_adj = ox.save_load.gdfs_to_graph(nodes_df, street_df)
    route = nx.shortest_path(G_adj, source=orig_node, target=target_node, weight='length')
    # By bringing it back to G, it gives us the route pic with orginal correct length.
    # but modified to consider crime data by taking route
    route_graph = ox.plot_route_folium(G, route, popup_attribute='length')

    folium.Marker(location=curr, popup=folium.Popup(curr_loc.title()),\
        icon=folium.Icon(color='red')).add_to(route_graph)

    folium.Marker(location=dest, popup=folium.Popup(destination.title()),\
        icon=folium.Icon(color='blue')).add_to(route_graph)

    filepath = 'safe_route/static/route_graph.html'
    route_graph.save(filepath)
    IFrame(filepath, width=600, height=500)

    return G_adj, route
