# !/usr/bin/env python3
""" A Python module for retrieving US weather data from a service.

This module demonstrates how to perform web requests against a service.
The free National Weather Service API was chosen because it does not
require an account or registration.

National Weather Service API (United States Only):
https://www.weather.gov/documentation/services-web-api
The 'Examples' tab demonstrates forecasts for Topeka, Kansas.

Additional location latitudes and longitudes can be found here:
https://www.latlong.net

# Sample usage with the locations.py module
import locations as loc
import us_weather as usw
latitude, longitude = loc.locations['Cleveland, Ohio']
usw.show_forecast(latitude, longitude)

History:
01.00 2024-Jun-25 Scott S. Initial release.

MIT License

Copyright (c) 2024 TigerPointe Software, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

If you enjoy this software, please do something kind for free.

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

import requests


def get_forecast(office, grid_x, grid_y):
    """ Gets the forecast periods for a set of grid points.
    Parameters
    office : the office grid identifier
    grid_x : the grid-x point
    grid_y : the grid-y point
    """
    url = 'https://api.weather.gov/gridpoints/{off}/{gx},{gy}/forecast'
    url = url.format(off=office, gx=grid_x, gy=grid_y)
    print(url)
    response = requests.get(url)
    data = response.json()
    properties = data['properties']
    return properties['periods']


def get_gridpoints(latitude, longitude):
    """ Gets the grid points for a set of coordinates.
    Parameters
    latitude  : the latitude coordinate
    longitude : the longitude coordinate
    """
    url = 'https://api.weather.gov/points/{lat},{lon}'
    url = url.format(lat=latitude, lon=longitude)
    print(url)
    response = requests.get(url)
    data = response.json()
    properties = data['properties']
    return properties['gridId'], properties['gridX'], properties['gridY']


def show_forecast(latitude=39.7456, longitude=-97.0892, period=0):
    """ Shows the forecast for a specified set of coordinates and period.
    Parameters
    latitude  : the latitude coordinate (defaults to the API example value)
    longitude : the longitude coordinate (defaults to the API example value)
    period    : the 7-day today/tonight period number (range 0-13)
                0 = today, 1 = tonight, 2 = tomorrow, 3 = tomorrow night, ...
    """
    grid_id, grid_x, grid_y = get_gridpoints(latitude, longitude)
    periods = get_forecast(grid_id, grid_x, grid_y)
    print('Forecast for',
          grid_id,
          periods[period]['name'])
    print('Temperature:  ',
          periods[period]['temperature'],
          periods[period]['temperatureUnit'])
    if periods[period]['probabilityOfPrecipitation']['value'] is not None:
        print('Precipitation:',
              periods[period]['probabilityOfPrecipitation']['value'],
              '% Probability')
    print('Wind Speed:   ',
          periods[period]['windSpeed'],
          periods[period]['windDirection'])
    print(periods[period]['shortForecast'])
    print(periods[period]['detailedForecast'])
    print()


# Start the program interactively
if __name__ == '__main__':

    # Define my selected coordinate locations (latitude and longitude)
    my_locations = {
        'Boston, Massachusetts': (42.361145, -71.057083),
        'Cleveland, Ohio':       (41.505493, -81.681290),
    }

    # Display the forecast data for my selected locations
    for key in my_locations.keys():
        print(key)
        latitude, longitude = my_locations[key]
        show_forecast(latitude, longitude)
    input('Press ENTER to Continue: ')
