#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import time
import datastore
import sys
import mysql.connector as mariadb
import logging
import simplejson as json
logging.basicConfig(filename='api.log',level=logging.DEBUG)

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

## AUTH STUFF ###

@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
## 404 handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

## Function to add URI to each requests
def make_public_reading(reading):
    new_reading = {}
    for field in reading:
        if field == 'id':
            new_reading['uri'] = url_for('get_reading', reading_id=reading['id'], _external=True)
        else:
            new_reading[field] = reading[field]
    return new_reading


## Routes
## /weather/api/v1/readings  GET ALL
@app.route('/weather/api/v1/readings', methods=['GET'])
@auth.login_required
def get_tasks():
    #   return jsonify({'readings': [make_public_reading(reading) for reading in readings]})
    return jsonify({'Readings': datastore.getReadings(2)})


@app.route('/weather/api/v1/readings/<int:reading_id>', methods=['GET'])
def get_task(reading_id):
    reading = [reading for reading in readings if reading['id'] == reading_id]

    if len(reading) == 0:
        abort(404)
    return jsonify({'reading': reading[0]})


@app.route('/weather/api/v1/readings', methods=['POST'])
def create_reading():
    status = 0
    logging.info('Started create_reading()')


    req_json = request.get_json()

    try:

        mariadb_connection = mariadb.connect(user='username', password='password', database='weather')

        cursor = mariadb_connection.cursor()

        cursor.execute("INSERT INTO reading (angle_x,angle_y,angle_z,Latitude,Longitude,TimeStamp) VALUES (%s,%s,%s,%s,%s,NOW())", (req_json['angle_x'],req_json['angle_y'],req_json['angle_z'],req_json['Latitude'],req_json['Longitude']))

        mariadb_connection.commit()

    except mariadb.Error as error:
        logging.error("Error: {}".format(error))
        return jsonify({'status': 'failed'}), 400

    except IOError as e:
        logging.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        return jsonify({'status': 'failed'}), 400

    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        return jsonify({'status': 'failed'}), 400

    # if all is good
    return jsonify({'status': 'succeeded'}), 201
@app.route('/hello', methods=['POST'])
def index():
   mariadb_connection = mariadb.connect(user='username', password='password', database='weather')

        cursor = mariadb_connection.cursor()

        cursor.execute("SELECT * FROM weather.reading")

   row_headers=[x[0] for x in cursor.description] #this will extract row headers
   rv = cursor.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json.dumps(json_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
