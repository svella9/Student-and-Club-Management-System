from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mypassword@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
db = SQLAlchemy(app)

@app.route('/')
def hello():
	return "Hello World!!"

if __name__ == '__main__':
	app.run(debug = True)