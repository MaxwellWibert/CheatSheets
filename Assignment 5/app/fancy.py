from flask import Flask, render_template, url_for, request
import datetime

app = Flask(__name__)

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

count = 0
@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    global count
    if(request.method == 'GET'):
        return render_template('clicker.html', count=count)
    elif(request.method == 'POST'):
        count += 1
        return render_template('clicker.html')

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




