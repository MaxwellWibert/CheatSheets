from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# creates a Counter table ORM in sqlalchemy
class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<Counter {self.id}, Count: {self.value}>'

db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clock')
def clock():
    #Gets the date of now
    t = datetime.datetime.now()
    date = t.strftime("%A, %B %d of %Y")
    #Gets the time of now
    time = t.strftime("%I:%M %p")
    #Renders template using variables
    return render_template('clock.html', date=date, time=time)

# Creates a counter and adds it to the database
counter = Counter(value=0)
db.session.add(counter)
db.session.commit()

@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    #gets counter
    counter = Counter.query.all()[0]
    if(request.method == 'GET'):
        count = counter.value
        return render_template('clicker.html', count=count)
    elif(request.method == 'POST'):
        counter.value += 1
        db.session.commit()
        count = counter.value
        return "count variable updated"

@app.route('/facts')
def people():
    return render_template('facts.html')

@app.route('/facts/<string:input>')
def show_person(input):
    return {
        'input' : input,
        'length': len(input),
        'uppercase': input.upper()
    }




