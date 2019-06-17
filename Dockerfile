FROM python:2.7-alpine
RUN apk --no-cache add build-base python-dev
WORKDIR /opt
COPY . /opt/
pip install -r requirements.txt
RUN python setup.py install
RUN sqlite3 user.db < user-schema.sql
CMD ["python run_app.py"]
