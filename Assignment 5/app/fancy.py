from flask import Flask, render_template, url_for, request
from MySQLdb import _mysql
import datetime

# connects to database
db = _mysql.connect(host="localhost", db="mydb")


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
db.query("""CREATE TABLE Clickers (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL
    Value int,
    PRIMARY KEY (ID)
)""")

db.query("""INSERT INTO Clickers (Name, Value)
VALUES (1, 'myclicker', 0)""")


@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    if(request.method == 'GET'):
        db.query("""SELECT value
        FROM Clickers
        WHERE Name = 'myclicker'""")
        count = db.store_result()
        return render_template('clicker.html', count=count)
    elif(request.method == 'POST'):
        db.query("""UPDATE Clickers
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




