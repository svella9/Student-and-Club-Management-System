from flask import Flask, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mypassword@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pesfacultyadvisor.sepro2017@gmail.com'
app.config['MAIL_PASSWORD'] = 'adminpesfacultyadvisor'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def hello():
	return "Hello World!!"

@app.route('/Student/register', methods = ['POST'])
def student_register():
	from University import Student, Faculty, Student_credential, Faculty_credential

	if request.method == 'POST':
		usn = request.form['usn']
		name = request.form['name']
		sem = request.form['sem']
		dept = request.form['dept']
		email = request.form['email']
		mob = request.form['mob']
		password = request.form['password']

		#Create a student object to insert into the Student table
		student = Student(usn, name, sem, dept, email, mob)
		student_credential = Student_credential(usn, password)

		db.session.add(student)
		db.session.add(student_credential)
		db.session.commit()

		return 'Student Record added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/Faculty/register', methods = ['POST'])
def faculty_register():
	from University import Student, Faculty, Student_credential, Faculty_credential

	if request.method == 'POST':
		fid = request.form['fid']
		name = request.form['name']
		dept = request.form['dept']
		email = request.form['email']
		mob = request.form['mob']
		password = request.form['password']

		#Create a faculty object to insert into the Faculty table
		faculty = Faculty(fid, name, dept, email, mob)
		faculty_credential = Faculty_credential(fid, password)

		db.session.add(faculty)
		db.session.add(faculty_credential)
		db.session.commit()

		return 'Faculty Record added successfully!!'

	else:
		#Bad Request
		abort(400)


@app.route('/notify/<int:semester>')
def send_notification(semester):
	"""Send notification to all students belonging to a particular semester"""

	from University import Student
	#query to retrieve students
	students = Student.query.filter_by(sem = semester).all()
	#keep only the email-id of the students
	students = list(map(lambda x : x.email, students))

	msg = Message('Meeting Schedule Notification.',
			sender = 'pesfacultyadvisor.sepro2017@gmail.com',
			recipients = students)
	msg.body = "Dear Student\n A meeting is scheduled on so and so date.\n We request you to attend the meeting."
	mail.send(msg)
	return "Notification Sent!!"


if __name__ == '__main__':
	app.run(debug = True)