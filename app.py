from flask import Flask, render_template, jsonify, request
import MySQLdb


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
@app.route('/employee')
def employee():
	db = MySQLdb.connect(host="127.0.0.1",
					 port=3308,
                     user="root",
                     passwd="root",
					 database="hr_employees")
	cursor = db.cursor()
	sql = """SELECT * FROM employees WHERE Id = 5"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		print (str(row[0]))
   	db.commit()
	db.close()
	return render_template('employee.html')

if __name__ == '__main__':
	app.run(debug = True) #continuous debugging 
