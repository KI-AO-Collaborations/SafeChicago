from django.shortcuts import render
from django import forms
import dijkstra_nocom
import dijkstra_com

community_areas_lst = [
        'ROGERS PARK', 'WEST RIDGE', 'UPTOWN',
        'LINCOLN SQUARE', 'NORTH CENTER', 'LAKE VIEW',
        'LINCOLN PARK', 'NEAR NORTH SIDE', 'EDISON PARK',
        'NORWOOD PARK', 'JEFFERSON PARK', 'FOREST GLEN',
        'NORTH PARK', 'ALBANY PARK', 'PORTAGE PARK',
        'IRVING PARK', 'DUNNING', 'MONTCLARE',
        'BELMONT CRAGIN', 'HERMOSA', 'AVONDALE',
        'LOGAN SQUARE', 'HUMBOLDT PARK', 'WEST TOWN', 'AUSTIN',
        'WEST GARFIELD PARK', 'EAST GARFIELD PARK',
        'NEAR WEST SIDE', 'NORTH LAWNDALE', 'SOUTH LAWNDALE',
        'LOWER WEST SIDE', 'LOOP', 'NEAR SOUTH SIDE',
        'ARMOUR SQUARE', 'DOUGLAS', 'OAKLAND', 'FULLER PARK',
        'GRAND BOULEVARD', 'KENWOOD', 'WASHINGTON PARK',
        'HYDE PARK', 'WOODLAWN', 'SOUTH SHORE', 'CHATHAM',
        'AVALON PARK', 'SOUTH CHICAGO', 'BURNSIDE',
        'CALUMET HEIGHTS', 'ROSELAND', 'PULLMAN',
        'SOUTH DEERING', 'EAST SIDE', 'WEST PULLMAN',
        'RIVERDALE', 'HEGEWISCH', 'GARFIELD RIDGE',
        'ARCHER HEIGHTS', 'BRIGHTON PARK', 'MCKINLEY PARK',
        'BRIDGEPORT', 'NEW CITY', 'WEST ELSDON', 'GAGE PARK',
        'CLEARING', 'WEST LAWN', 'CHICAGO LAWN',
        'WEST ENGLEWOOD', 'ENGLEWOOD', 'GREATER GRAND CROSSING',
        'ASHBURN', 'AUBURN GRESHAM', 'BEVERLY',
        'WASHINGTON HEIGHTS', 'MOUNT GREENWOOD', 'MORGAN PARK',
        'OHARE', 'EDGEWATER']
        
threshold_lst = ['default', 'safer', 'safest']


def create_dropdown(choices):
    '''
    Creates a dropdown menu using the provided options.
    Inputs:
        choices (lst): a list of options
    '''
    return [(x, x) for x in choices]

COMMUNITY_AREAS = create_dropdown(['BETWEEN COMMUNITIES (SLOWER)'] + sorted(
community_areas_lst))
THRESHOLDS = create_dropdown(threshold_lst)


class ShortPathForm(forms.Form):
    '''
    A class used to create a form that allows for the collection and
    validation of user-inputted data.
    '''
    cur_loc = forms.CharField(
    label = 'Point of Departure',
    help_text = '1100 E 57th St, Chicago, IL 60637',
    required = True)
    dest = forms.CharField(
    label = 'Destination',
    help_text = '1100 E 57th St, Chicago, IL 60637',
    required = True)
    threshold = forms.ChoiceField(
    label = 'Safety Threshold',
    choices = THRESHOLDS,
    required = True)
    comm_area = forms.ChoiceField(
    label = 'Community Area',
    choices = COMMUNITY_AREAS,
    required = False)

def index(request):
    '''
    Used to generate the content of the html document.
    '''
    if request.method == 'GET':
        form = ShortPathForm(request.GET) 
    context = {}
    context['form'] = form
    if form.is_valid():
        current_loc = form.cleaned_data['cur_loc']
        destination = form.cleaned_data['dest']
        thresh = form.cleaned_data['threshold']
        if form.cleaned_data['comm_area'] != 'BETWEEN COMMUNITIES (SLOWER)':
            community_area = form.cleaned_data['comm_area']
            try:
                context['directions'] = dijkstra_com.get_route(
                community_area,thresh,current_loc,destination)
            except Exception as e:
                print(e)
                context['err'] = '''Please ensure you have inputted valid 
                locations and have selected the right community area!'''
        else:
            try:
                context['directions'] = dijkstra_nocom.get_route(thresh, 
                current_loc, destination)
            except Exception as e:
                print(e)
                context['err'] = 'Please ensure you have inputted valid locations'

    return render(request, 'index.html', context)
