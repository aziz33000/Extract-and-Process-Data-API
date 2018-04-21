from flask import Flask, render_template

app = Flask(__name__)
 #continuous debugging 

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
	app.run(debug = True) #continuous debugging d