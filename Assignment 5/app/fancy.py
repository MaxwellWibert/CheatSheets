from flask import Flask, render_template, url_for, request
import sqlite3
import datetime
import pandas as pd

app = Flask(__name__)

connection = sqlite3.connect('clicker.db', check_same_thread=False)
cursor = connection.cursor()



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



# Checks to see if Clicks table exists. If not, creates one

cursor.execute("CREATE TABLE IF NOT EXISTS Clicks(ID INTEGER, TIME varchar(255) NOT NULL, PRIMARY KEY (ID))")


# GIVE WARNING ON SQL INJECTION

@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    if(request.method == 'GET'):
        df = pd.read_sql_query("""SELECT * FROM Clicks""", connection)
        print(df.head())
        count = len(df.index)
        return render_template('clicker.html', count=count)
    elif(request.method == 'POST'):
        cursor.execute("INSERT INTO Clicks(TIME) VALUES(unixepoch('now'));")
        return "count variable updated"

@app.route('/facts')
def facts_page():
    return render_template('facts.html')

@app.route('/facts/<string:input>')
def facts_api(input):
    return {
        'input' : input,
        'length': len(input),
        'uppercase': input.upper()
    }




