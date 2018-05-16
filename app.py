from flask import Flask, render_template, jsonify, request
import MySQLdb
import tensor
import json


app = Flask(__name__)

criteres = ["Id","BusinessTravel","DailyRate","DistanceFromHome","MonthlyIncome","PerformanceRating"]

###View Part
@app.route('/')
def index():
	
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/api')
def api():
	return render_template('api.html')

###API Part


##################### VERIFICATION ####################

#More monthly incomes means more performance rating.
@app.route('/rule1', methods=['GET'])
def verifrule1():
	moreIncomeMoreAttrition = 0
	notTrue = 0
	avgAttrition = 0.0
	avgIncome = 0.0

	#connect and extract Database
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	moyenneSql = """SELECT AVG(PerformanceRating), AVG(MonthlyIncome) FROM employees"""
	sql = """SELECT PerformanceRating,MonthlyIncome FROM employees"""
	cursor.execute(moyenneSql)
	moyennes = cursor.fetchall()
	for row in moyennes:
		avgAttrition = (float)(row[0])
		avgIncome = (float)(row[1])
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		attrition = (float)(row[0])
		income = int(row[1])
		if(attrition>2.5)and(income>avgIncome):
			moreIncomeMoreAttrition = moreIncomeMoreAttrition + 1
		else:
			notTrue = notTrue + 1
	db.commit()
	cursor.close()
	db.close()
	pourcentage = moreIncomeMoreAttrition / (moreIncomeMoreAttrition+notTrue) * 100
	return jsonify({'resultat':str(pourcentage)})

#less distance from home means more performance rating.
@app.route('/rule2', methods=['GET'])
def verifrule2():
	moreDistanceLessperformance = 0
	notTrue = 0
	avgDistance = 0.0
	avgAttrition = 0.0

	#connect and extract Database
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	moyenneSql = """SELECT AVG(PerformanceRating), AVG(DistanceFromHome) FROM employees"""
	sql = """SELECT PerformanceRating,DistanceFromHome FROM employees"""
	cursor.execute(moyenneSql)
	moyennes = cursor.fetchall()
	for row in moyennes:
		avgAttrition = (float)(row[0])
		avgDistance = (float)(row[1])
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		attrition = (float)(row[0])
		distance = int(row[1])
		if(attrition>2.5)and(distance<avgDistance):
			moreDistanceLessperformance = moreDistanceLessperformance + 1
		else:
			notTrue = notTrue + 1
	db.commit()
	cursor.close()
	db.close()
	pourcentage = moreDistanceLessperformance / (moreDistanceLessperformance+notTrue) * 100
	return jsonify({'resultat':str(pourcentage)})

#More business travel mean more performance rating.
@app.route('/rule3', methods=['GET'])
def verifrule3():

	totalTravel = 0
	totalNonTravel = 0
	totalFrequently = 0
	avgAttritionTravel = 0.0
	avgAttritionNonTravel = 0.0
	avgAttritionFrequently = 0.0

	#connect and extract Database
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	moyenneSqlTravel = """SELECT AVG(PerformanceRating),COUNT(BusinessTravel) FROM employees WHERE BusinessTravel ="Travel_Rarely" """
	moyenneSqlNone = """SELECT AVG(PerformanceRating),COUNT(BusinessTravel) FROM employees WHERE BusinessTravel ="Non-Travel" """
	moyenneSqlAlot = """SELECT AVG(PerformanceRating),COUNT(BusinessTravel) FROM employees WHERE BusinessTravel ="Travel_Frequently" """
	cursor.execute(moyenneSqlTravel)
	moyennes1 = cursor.fetchall()
	for row in moyennes1:
		avgAttritionTravel = (float)(row[0]) 
		totalTravel = (int)(row[1])
		print (avgAttritionTravel, totalTravel)

	cursor.execute(moyenneSqlNone)
	moyennes2 = cursor.fetchall()
	for row in moyennes2:
		avgAttritionNonTravel = (float)(row[0])
		totalNonTravel = (int)(row[1])
		print (avgAttritionNonTravel, totalNonTravel)

	cursor.execute(moyenneSqlAlot)
	moyennes3 = cursor.fetchall()
	for row in moyennes3:
		avgAttritionFrequently = (float)(row[0]) 
		totalFrequently = (int)(row[1])
		print (avgAttritionFrequently , totalFrequently) 

	db.commit() 
	cursor.close()
	db.close()
	return jsonify({'travel-frequently':str(avgAttritionFrequently*100/5),'travel-rarely':str(avgAttritionTravel*100/5),'non-travel':str(avgAttritionNonTravel*100/5)})

#More dailywork mean less performance rating.
@app.route('/rule4', methods=['GET'])
def verifrule4():
	moreDailyLessperformance = 0
	notTrue = 0
	avgDaily = 0.0
	avgAttrition = 0.0

	#connect and extract Database
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	moyenneSql = """SELECT AVG(PerformanceRating), AVG(DailyRate) FROM employees"""
	sql = """SELECT PerformanceRating,DailyRate FROM employees"""
	cursor.execute(moyenneSql)
	moyennes = cursor.fetchall()
	for row in moyennes:
		avgAttrition = (float)(row[0])
		avgDaily = (float)(row[1])
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		attrition = (float)(row[0])
		daily = int(row[1])
		if(attrition<avgAttrition)and(daily>avgDaily):
			moreDailyLessperformance = moreDailyLessperformance + 1
		else:
			notTrue = notTrue + 1
	print(notTrue,moreDailyLessperformance)
	db.commit()
	cursor.close()
	db.close()
	pourcentage = moreDailyLessperformance / (moreDailyLessperformance+notTrue) * 100
	return jsonify({'resultat':str(pourcentage)})

########################################################

##################### DATABASE #########################
@app.route('/employee', methods=['GET'])
def employeeAll():
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	dictFeatures = {}
	cursor = db.cursor()
	base = ','.join(criteres)
	sql = """SELECT """+ base +""" FROM employees"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		raw = {}
		fid = int(row[0])
		for i in criteres:
			raw [str(i)] = row[criteres.index(str(i))]
		dictFeatures[fid] = row
	db.commit()
	db.close()
	return jsonify(dictFeatures)

@app.route('/addcritere/<critere>', methods=['PUT'])
def addCritere(critere):
	criteres.append(str(critere))
	print (criteres)
	return "ECHO: PUT"
##############################################################


##################### DASHBOARD ##############################


@app.route('/<string:crit>/<int:Id>', methods=['GET'])
def employeeOne(crit,Id):
	
	jsonInterne = {}
	jsonExterne = {}
	db = MySQLdb.connect(host="127.0.0.1", port=3308, user="root", passwd="root", database="hr_employees")
	cursor = db.cursor()
	base = ','.join(criteres)
	sql = """SELECT """+ base +""" FROM employees WHERE """+crit+"""="""+str(Id)
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		for i in criteres:
			fid = str(i)
			jsonInterne[fid] = row[criteres.index(str(i))]
		jsonExterne[(int)(row[0])] = jsonInterne
	db.commit()
	db.close()
	return jsonify(jsonExterne)

@app.route('/criteres', methods=['GET'])
def criteresAll():
	
	jsoni = {}
	jsoni["resultat"] = criteres
	return jsonify(jsoni)

@app.route('/test', methods=['POST'])
def api_test():
	dico = json.dumps(request.json)
	return "JSON Message: " + dico

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
	return jsonify({'resultat':'training done'})
	
#PUT / DELETE
if __name__ == '__main__':
	app.run(debug = True) #continuous debugging 
