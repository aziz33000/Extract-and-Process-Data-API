from flask import Flask, render_template, jsonify, request
import mysql.connector
import tensor


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
@app.route('/employee', methods=['GET'])
def employeeAll():
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	dictFeatures = {}
	cursor = db.cursor()
	sql = """SELECT * FROM employees"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		fid = int(row[0])
		dictFeatures[fid] = row
	db.commit()
	db.close()
	return jsonify({'result' : 'output'})

@app.route('/employee/<int:Id>', methods=['GET'])
def employeeOne(Id):
	return jsonify({'languages': str(Id) })

@app.route('/createModel')
def createModelTensorflow():
	dictFeatures = {}
	#connect and extract Database
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	sql = """SELECT * FROM employees"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		fid = int(row[0])
		dictFeatures[fid] = row
	db.commit()
	cursor.close()
	db.close()
	tensor.trainModel(dictFeatures)
	return ({'jsonKey':'json'})
	
#PUT / DELETE
if __name__ == '__main__':
	app.run(debug = True) #continuous debugging 
