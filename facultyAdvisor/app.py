from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mypassword@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pesfacultyadvisor.sepro2017@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def hello():
	#return "Hello World!!"
	return render_template('home.html')

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
	#print('sending Message', students)
	msg = Message('Meeting Schedule Notification.',
			sender = 'pesfacultyadvisor.sepro2017@gmail.com',
			recipients = students)
	#print('Object created!')
	msg.body = "Dear Student\n A meeting is scheduled on so and so date.\n We request you to attend the meeting."
	mail.send(msg)

	return "Notification Sent!!"

@app.route('/Student/savefeedback', methods = ['POST'])
def student_save_feedback():
	"""Save the feedback/issues given by the student in the database"""
	from University import Student, Student_feedback
	if request.method == 'POST':
		usn = request.form['usn']
		feedback = request.form['feedback']

		#get the student object from the table bearing the usn
		q = Student.query.filter_by(usn = usn).first()
		#pass the student object to the Student_feedback class for the purpose of foreign key establishment.
		student_feedback = Student_feedback(feedback = feedback, student = q)
		db.session.add(student_feedback)
		db.session.commit()
		return "Feedback Submitted successfully!"

	else:
		abort(400)

@app.route('/Faculty/savefeedback', methods = ['POST'])
def faculty_save_feedback():
	"""Save the feedback given by the faculty for a student in the database"""
	from University import Student, Faculty, Faculty_feedback
	if request.method == 'POST':
		fid = request.form['fid']
		student_usn = request.form['student_usn']
		feedback = request.form['feedback']

		#get the faculty object bearing the fid
		faculty = Faculty.query.filter_by(fid = fid).first()
		#get the student object bearing the usn
		student = Student.query.filter_by(usn = student_usn).first()
		#pass the faculty and student object to the Faculty_feedback class for the purpose of foreign key establishment.
		faculty_feedback = Faculty_feedback(feedback = feedback, faculty = faculty, student = student)
		db.session.add(faculty_feedback)
		db.session.commit()
		return "Your feedback is submitted!"

	else:
		abort(400)