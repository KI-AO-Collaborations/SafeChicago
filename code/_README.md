README
=========================== 

## Libraries Used
- OSMNX
- NetworkX
- pandas
- numpy
- matplotlib
- geopandas
- folium 
- re
- time
- datetime
- math
- dominate
- schedule
- pickle
- base64

## Data Sources / API
- Chicago Data Portal
- Open Street Map 
- Google Maps API
- Open Weather Map
- Sodapy

## Explanation of Our codes
<!-- MarkdownTOC autolink="true" levels="1,2,3,4,5,6" bracket="round" style="unordered" indent="    " autoanchor="false" markdown_preview="github" -->

- [\(1\) Safety Score](#1-safety-score)
- [\(2\) Dijkstra's Algorithm](#2-dijkstra-algorithm)
- [\(3\) Folium Map](#3-folium-map)
- [\(4\) Safe Chicago Folder](#4-safe-chicago-folder)
- [\(5\) Documentation](#5-documentation)

Click on the pink highlights to open the files and folders below.

<!-- toc -->

## (1) Safety Score

Construction of safety scores associated to nodes

### [`generate_data.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/generate_data.py)

Generate files used to construct safety_score_com_dict, which is a dictionary that maps community areas to dictionary of key as node_id and value as corresponding safety score. 

**The following are files called by generate.py:**

#### [`community_boundaries.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/community_boundaries.py)

Creates com_Gs (dictionary), which maps community area to boundary geodataframe.

#### [`cleaned_dataset_crime.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/cleaned_dataset_crime.py)

Creates com_dict (dictionary), which maps community area to cleaned dataframe 
ready to be used to get safety scores.

#### [`recent_data.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/recent_data.py)

Pulls recent data from Chicago Data Portal and appends it to com_dict.

#### [`safety_score.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safety_score.py)

Creates safety_score_com_dict (dictionary), which maps community areas to dictionary of key as node_id and value as corresponding safety score.

## (2) Dijkstra Algorithm

Finding the shortest path from current location to destination location considering safety threshold. 

### [`dijkstra_com.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safechicago/dijkstra_com.py)

Gets direction from current to destination location given threshold of safety level. The current and destination location must be in the same community area. 

### [`dijkstra_nocom.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safechicago/dijkstra_nocom.py)

Gets direction from current to destination location given threshold of safety level. The current and destination location do not have to be in the same community area. However, it takes more time to find the path from current to destination location.

**The following are files called by dijkstra.py:**

#### [`directions.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safechicago/directions.py)

Gets direction from current location to destination location using Google Maps Directions API.

#### [`get_pctiles`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/get_pctiles.py)

Gets 25, 50, 75 percentile of safety scores considering all situations such as season, month, day of time. 

#### [`google_maps.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safechicago/google_maps.py)

Gets the location in terms of latitutude and longitude given current string information of location. 

### [`daily_updates.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/daily_update.py)

Calls generate_data.py and updates safety score based on time of day and season. Each morning pulls recent data through recent_data.py

### [`recent_data.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/recent_data.py)

Called in generate_data.py to pull recent data from Chicago Data Portal, and appends it to com_dict. 

## (3) Folium Map

### [`crime_stat_map.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/crime_stat_map.py)

Creates folium heat map of crime in different community areas of chicago. Includes selection feature of 2017, 2018, 2019. 

## (4) Safe Chicago Folder
Includes files required to generate our website. 

### safe_route Folder

#### [`static`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/tree/master/safechicago/safe_route/static)

Contains all static files; includes css file used to style the html document.

#### [`Templates`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/tree/master/safechicago/safe_route/templates)

Contains the html file used to generate the website.

#### [`views.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/safechicago/safe_route/views.py)

Used to render the template; creates form used in website and stores output of dijkstra.py and passes them as variable to the template.

## (5) Documentation

### [`doc.py`](https://mit.cs.uchicago.edu/kirizawa/cmsc122-project-kei-adam-shyam-sway/blob/master/docfiles/doc.py)

Creates html documentaion explaining our project to user of website. 

