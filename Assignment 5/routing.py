from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is a home page'

@app.route('/about')
def about():
    return 'This is an about page'

@app.route('/about/team')
def team():
    return 'This is about the team, nested in the about route'

@app.route('/person/<name>')
def show_person(name):
    return f'A person named {name} went to the moon'