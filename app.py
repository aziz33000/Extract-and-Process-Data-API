from flask import Flask, render_template, flash, redirect, url_for
import mysql.connector
import sys

def create_connection():
	cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='employees')
	cursor = cnx.cursor()
	query = ("SELECT * FROM employees ")
	cursor.execute(query)
	for (Age) in cursor:
  		print("{} was hired on".format(Age))

	cursor.close()
	cnx.close()


app = Flask(__name__)

#View Part
@app.route('/')
def index():
	
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/api')
def api():
	return render_template('api.html')

#API Part


if __name__ == '__main__':
	app.run(debug = True) #continuous debugging 