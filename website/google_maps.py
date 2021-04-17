'''
Purpose:
    Uses Google Maps API to get location data.
'''
import googlemaps


def get_lat_lng(location):
    '''
    Purpose:
        Gets latitude and longitude from the name of location using Google
        Maps geocode AP
    Inputs:
        location (string): name of the location
    Outputs:
        lat, lng (float): gives floats of latitutde and longitude information
    '''
    gmaps = googlemaps.Client(key='AIzaSyAmmm3Lc1n897ijWvvFuyg1TR-kixbAvAQ')
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return lat, lng
