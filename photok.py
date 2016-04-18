from flask import Flask
from flask import render_template

import os

app = Flask(__name__)

# some configs depending on if we're running the code locally or remotely
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['OPENSHIFT_MYSQL_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///tmp/testdb.db"
    app.config['DEBUG'] = True

@app.route('/')

def homepage():
    return render_template('pages/homepage.html')

@app.route('/link')
def link():
    return render_template('pages/page.html')

if __name__ == '__main__':
    app.run(debug=True)
