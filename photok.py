from flask import Flask
import os

app = Flask(__name__)

# some configs depending on if we're running the code locally or remotely
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['OPENSHIFT_MYSQL_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///tmp/testdb.db"
    app.config['DEBUG'] = True



@app.route('/')
def hello_world():
    return 'Hello <a href="laurent">Laurent</a>, Sijmen and Julius!'

@app.route('/laurent')
def laurent_fun():
    return 'Hello Laurent only!'

@app.route('/sijmen')
def sijmen_fun():
    return 'Hello Laurent, Sijmen and Julius!'

@app.route('/julius')
def julius_fun():
    return 'Hello <b>Julius</b>!'


if __name__ == '__main__':
    app.run()
