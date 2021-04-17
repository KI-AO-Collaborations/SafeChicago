'''
Purpose:
    Get node percentiles based on safety scores
'''
import pickle
import numpy as np
import osmnx as ox
import safety_score


def get_pctiles(plot=False):
    '''
    Purpose:
        Get node percentiles based on safety scores
    Inputs:
        plot: whether to plot histogram
    Returns:
        (tuple): 25th, 50th, 75th percentiles of scores;
            mean score, min score, max score
    '''
    seasons = ['summer', 'fall', 'winter', 'spring']
    times_of_day = ['day', 'night']
    com_Gs = pickle.load(open('safechicago/pickle_files/com_Gs.p', 'rb'))
    safety_scores = {}
    for season in seasons:
        for time_of_day in times_of_day:
            com_dict = pickle.load(open('safechicago/pickle_files/com_dict.p',\
                'rb'))
            print('Percentile com dict loaded for ' + season + ' and ' + time_of_day)
            # Must reload com_dict each iteration to prevent
            # safety_score from overwriting data
            safety_score_com = safety_score.get_safety_score_com_dict\
                                (com_dict, time_of_day, season)

            for com, nodes in safety_score_com.items():
                safety_scores[com] = safety_scores.get(com, {})

                for node, score in nodes.items():
                    safety_scores[com][node] = safety_scores[com].get(node, [])
                    safety_scores[com][node].append(score)

    scores = []
    max_nodes = []
    for com_name, com in safety_scores.items():
        max_node = 0
        max_score = 0
        com_scores = []
        for node, score in com.items():
            avg_score = round(sum(score) / len(score), 2)
            scores.append(avg_score) # Get avg score for each node
            com_scores.append(avg_score)
            if avg_score > max_score:
                max_node = node
                max_score = avg_score

        if plot:
            com_G = com_Gs[com_name]
            nodes_df, street_df = ox.graph_to_gdfs(com_G, nodes=True,\
                edges=True)
            lat = nodes_df[nodes_df['osmid'] == max_node]['y']
            lng = nodes_df[nodes_df['osmid'] == max_node]['x']
            max_nodes.append((lat, lng, max_score))

    scores = np.array(scores)
    low = np.percentile(scores, 25)
    medium = np.percentile(scores, 75)
    high = np.percentile(scores, 90)
    mean_val = sum(scores) / len(scores)
    min_val = min(scores)
    max_val = max(scores)

    return np.array([low, medium, high, mean_val, min_val, max_val]), max_nodes
