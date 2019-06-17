import os

from api._user_data import app


if __name__ == '__main__':
    app.debug = True
    app.config['DATABASE_NAME'] = 'user.db'
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
