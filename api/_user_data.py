import json
import sqlite3
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE
import arrow
from datetime import datetime

app = Flask(__name__)


@app.before_request
def before_request():
    try:
        #making connection with db.
        g.db = sqlite3.connect(app.config['DATABASE_NAME'])
    except Exception as e:
        error = json.dumps({'Exception': "Invalid db/table name"})
        return json_response(error, 400)

@app.route('/hello/')
def user_list():
    try:
        cursor = g.db.execute('SELECT id, user, dob FROM users;') # fetching all data from users table
        users = [{
            'id1': row[0],
            'user': row[1],
            'dob': row[2]
        } for row in cursor.fetchall()]

        return json_response(json.dumps(users))
    except Exception as e:
        error = json.dumps({'Exception': str(e)})
        return json_response(error, 400)

@app.route('/hello/<user_name>')
def user_detail(user_name):
    try:
        cursor = g.db.execute('SELECT id, user, dob FROM users where user=?',(user_name,)) #fetching users data by user name
        row=cursor.fetchone()
        if row is None:
            error = json.dumps({'error': 'This user is not available'})
            return json_response(error, 400)

        birth=str((row[2]))
        dateOfBirth = datetime.strptime(birth,'%Y-%m-%d')
        todayDate = datetime.today()
        if( todayDate.month == dateOfBirth.month and todayDate.day > dateOfBirth.day or todayDate.month > dateOfBirth.month ):
            nextBirthdayYear = todayDate.year + 1
        else:
            nextBirthdayYear = todayDate.year
        nextBirthday = datetime(nextBirthdayYear, dateOfBirth.month, dateOfBirth.day )
        diff = nextBirthday - todayDate
        days = diff.days + 1
        if days == 0:
            message = json.dumps({'message': 'Hello, '+user_name+'! Happy birthday!'})
        else:
            message = json.dumps({'message': 'Hello, '+user_name+'! Your birthday is in '+str(days)+' days'})
        return json_response(message, 200)
    except Exception as e:
        error = json.dumps({'Exception': str(e)})
        return json_response(error, 400)

@app.route('/hello/<user_name>', methods=['PUT'])
def user_create(user_name):
    try:
        if request.content_type != JSON_MIME_TYPE:
            error = json.dumps({'error': 'Invalid Content Type'})
            return json_response(error, 400)

        if user_name.isalpha():
            data = request.json
            if not all([data.get('dateOfBirth')]):
                error = json.dumps({'error': 'Missing field dateOfBirth'})
                return json_response(error, 400)
            dateOfBirth = arrow.get(str(data['dateOfBirth']))
            todayDate = arrow.get(datetime.today().strftime('%Y-%m-%d'))
            delta = (todayDate-dateOfBirth)
            if delta.days < 0:
                error = json.dumps({'error': 'Date Of Birth must be before todays date'})
                return json_response(error, 400)
            # save data into users table
            query = ('INSERT INTO users ("user", "dob") '
            'VALUES (:user, :dob);')
            params = {
            'user': user_name,
            'dob': data['dateOfBirth']
            }
            g.db.execute(query, params)
            g.db.commit()
            return json_response(status=204)
        else:
            error = json.dumps({'error': 'Invalid user name, it must contains only letters'})
            return json_response(error, 400)
    except Exception as e:
        error = json.dumps({'Exception': str(e)})
        return json_response(error, 400)
