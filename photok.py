from flask import Flask
app = Flask(__name__)

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
    return 'Hello Laurent, Sijmen and Julius!'


if __name__ == '__main__':
    app.run()
