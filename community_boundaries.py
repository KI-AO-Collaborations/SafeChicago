'''
Purpose: Get community boundary area information as polygon shapefile.
'''
import osmnx as ox

def get_Gs(chicago_boundaries, community_areas):
    '''
    Purpose:
        Construct dictionary that maps community areas to its boundary polygon geoframe.
    Inputs:
        chicago_boundaries (GeoDataFrame): data on community area boundaries
        community_areas (dictionary): dictionary linking community area names to
            community area numbers
    Outputs:
        com_Gs (dictionary): maps community area to boundary shapefile.
        (Ex) com_Gs = {'HYDE PARK': hyde_park polygon, 'DOUGLAS': douglas polygon}
    '''

    com_Gs = {}
    for com in community_areas:
        mission_district = chicago_boundaries[chicago_boundaries['community'] == com]
        polygon = mission_district['geometry'].iloc[0]
        G = ox.graph_from_polygon(polygon, network_type='walk')
        com_Gs[com] = G
        print('Community area generated: ', com)
    return com_Gs
