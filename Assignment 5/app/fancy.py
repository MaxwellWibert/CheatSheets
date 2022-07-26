from flask import Flask, render_template, url_for, request
import sqlite3
import datetime

connection = sqlite3.connect('clicker.db')
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



# Creates a counter and adds it to the database
cursor.execute("""CREATE TABLE Clickers (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL
    Value int,
    PRIMARY KEY (ID)
)""")

# GIVE WARNING ON SQL INJECTION
cursor.execute("""INSERT INTO Clickers (Name, Value)
VALUES (1, 'myclicker', 0)""")


@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    if(request.method == 'GET'):
        cursor.execute("""SELECT value
        FROM Clickers
        WHERE Name = 'myclicker'""")
        count = db.store_result()
        return render_template('clicker.html', count=count)
    elif(request.method == 'POST'):
        cursor.execute("""UPDATE Clickers
        SET Value = Value + 1
        WHERE Name = 'myclicker'""")
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




