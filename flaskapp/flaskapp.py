import json
from time import time
from random import random
from flask import Flask, render_template, make_response, request
import os
import json
from pymongo import MongoClient
from bson import json_util
from pymongo.cursor import CursorType
import requests
import geocoder

# API KEYS
API_KEY_TWITTER = ''
API_KEY_WEATHER = ''


# Set the mongo database
MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
collection_accelerometer = MongoClient(MONGO_DB_URL).accelerometer.measures


# Run the server
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

@app.route('/live-data')
def live_data():
    print "Begins to retrieve x, y, z from the Mongo database..."
    global collection_accelerometer
    cursor = collection_accelerometer.find({})
    try:
        #doc = cursor.next()
        doc = list(cursor)[-1]
        data = [[time() * 1000, int(doc['x'])], [time() * 1000, int(doc['y'])], [time() * 1000, int(doc['z'])]]
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return(response)
    except StopIteration:
        data = [[time() * 1000, 0], [time() * 1000, 0], [time() * 1000, 0]]
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return(response)


@app.route('/get_data', methods=['GET'])
def get_data():
    global collection_accelerometer
    x = request.args.get('x', '')
    y = request.args.get('y', '')
    z = request.args.get('z', '')
    coordinates = dict()
    coordinates['x'] = int(x)
    coordinates['y'] = int(y)
    coordinates['z'] = int(z)
    collection_accelerometer.insert(coordinates)
    return('Inserted !')


@app.route('/weather', methods=['GET'])
def weather_api_call():
    global API_KEY_WEATHER
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')

    # Make the call to the Open Weather API
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) +'&appid=' + str(API_KEY_WEATHER)
    r = requests.get(url)
    r = r.json()
    temp = r['main']['temp'] - 273.15
    pressure = r['main']['pressure']
    weather = r['weather'][0]['main']
    print('-------------')
    print('temp = ', str(temp))
    print('pressure = ', str(pressure))
    print('weather = ', str(weather))
    print('-------------')
    data = dict()
    data['temp'] = temp
    data['pressure'] = pressure
    data['weather'] = weather
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return(response)



@app.route('/geoloc', methods=['GET'])
def geoloc_api_call():
    ip_address = request.args.get('ip', '')

    # Make the call to the Open Weather API
    g = geocoder.ip(str(ip_address))
    data = dict()
    data['lat'] = g.lat
    data['lon'] = g.lng
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return(response)


@app.route('/tweet', methods=['GET'])
def twitter_api_call():
    global API_KEY_TWITTER
    tweet = str(request.args.get('text', ''))

    # Make the call to the twitter API through the Thingspeak API
    url = 'http://api.thingspeak.com/apps/thingtweet/1/statuses/update'
    r = requests.post(url, data = {'api_key':API_KEY_TWITTER, 'status':tweet})
    data = dict()
    data['resp'] = 'Tweet sent'
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return(response)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
