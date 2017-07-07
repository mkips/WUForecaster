#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import subprocess

'''hourly wetter warnings using the Wunderground API

for API information, see: https://www.wunderground.com/weather/api/
    
Request URL Format: GET http://api.wunderground.com/api/[api_key]/[features]/[settings]/q/[query].[format]
Request Example:    GET http://api.wunderground.com/api/94ec8af3a9a2d81b/hourly/q/Germany/Berlin.json
'''

def get_json_response(api_key, country, city):
    url = 'http://api.wunderground.com/api/{}/hourly/q/{}/{}.json'.format(api_key, country, city)

    response = urllib2.urlopen(url).read()
    return json.loads(response)

def print_forecast(json_data):
    forecast = json_data['hourly_forecast'][0]
    title = 'Forecast for {}:{}'.format(forecast['FCTTIME']['hour'], forecast['FCTTIME']['min'])
    message = '{} °C\n{}\n{} km/h from {}'.format(forecast['temp']['metric'], forecast['condition'], forecast['wspd']['metric'], forecast['wdir']['dir'])
    
    # notification expires after 120000 millisenconds (2 minutes)
    subprocess.Popen(['notify-send', '--expire-time=120000', title, message])

def print_warning(json_data):
    forecast = json_data['hourly_forecast'][0]
    no_warnings_for = ['Clear', 'Partly Cloudy']

    if forecast['condition'] not in no_warnings_for:
        print_forecast(json_data)

def main():
    if len(sys.argv) < 3:
        print 'Error: Please provide the neccessary information:'
        print 'WUForecaster/main.py Country City (warn-only)'
    else:
        api_key = 'YOUR_API_KEY'
        country = sys.argv[1]
        city = sys.argv[2]
        json_data = get_json_response(api_key, country, city)

        if len(sys.argv) > 3:
            if sys.argv[3] == 'warn-only':
                print_warning(json_data)
            else:
                print 'Error: Unexpected argument \'{}\''.format(sys.argv[3])
        else:
            print_forecast(json_data)


if __name__ == '__main__':
    main()
