SafeChicago
===========

## Project Overview
SafeChicago provides a visual map and step by step directions of the optimal path from location A to location B considering dynamically updated safety scores calculated using past and present crime data. We apply Dijkstra's algorithm on streets represented as network of nodes with modified values of edges based on safety scores. Also, we created an interactive map with crime information in Chicago.

## Instructions to Open Website
- Navigate to `./website`
- Open the website by typing `python3 manage.py runserver` in terminal

## Important Note:
- In order to save this in Github, some files were compressed into .zip format. Uncompress the following files before running to ensure the software runs properly:
- data/crime_data_2017.csv
- safechicago/pickle_files/adjusted_street_com.p
- safechicago/pickle_files/street_com.p
