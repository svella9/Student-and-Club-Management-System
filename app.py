from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
from sqlalchemy import and_, or_
from flask_mail import Mail, Message

app = Flask(__name__)
POSTGRES = {
	'user' : 'qxccmophyqzgyq',
	'pw' : '767a822d6490e361bd0ae575af9bdc992e2a80dae76061f189c658e6de864064',
	'db' : 'd5d9l9desafg81',
	'host' : 'ec2-184-73-159-137.compute-1.amazonaws.com',
	'port' : '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qxccmophyqzgyq:767a822d6490e361bd0ae575af9bdc992e2a80dae76061f189c658e6de864064@ec2-184-73-159-137.compute-1.amazonaws.com:5432/d5d9l9desafg81' % POSTGRES #'postgresql://postgres:mypassword@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)

mail_credentials = open('credentials.txt').read().split('\n')
#print(mail_credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mail_credentials[0]
app.config['MAIL_PASSWORD'] = mail_credentials[1]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def index():
	#return "Hello World!!"
	return render_template('FacultyAdvisor.html')

@app.route('/getStudentLogin/')
def getStudentLogin():
	return render_template('studentlogin.html')

@app.route('/getFacultyLogin/')
def getFacultyLogin():
	return render_template('facultylogin.html')	

@app.route('/getStudentRegistration/')
def getStudentRegistration():
	return render_template('studentregistration.html')	

@app.route('/getFacultyRegistration/')
def getFacultyRegistration():
	return render_template('facultyregistration.html')		

@app.route('/Student/register/', methods = ['POST'])
def student_register():
	from University import Student, Faculty, Student_credential, Faculty_credential
	try:
		if request.method == 'POST':
			usn = request.form['usn'].lower()
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

	except sqlalchemy.exc.IntegrityError:
		db.session.rollback()
		return "Account already exists.."

	#except:
	#	db.session.rollback()
	#	return "Cannot register user..."

@app.route('/Faculty/register/', methods = ['POST'])
def faculty_register():
	from University import Student, Faculty, Student_credential, Faculty_credential

	try:
		if request.method == 'POST':
			fid = request.form['fid'].lower()
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
	except sqlalchemy.exc.IntegrityError:
		db.session.rollback()
		return "Account already exists..."
	#except:
	#	db.session.rollback()
	#	return "Cannot register..."


@app.route('/notify/<int:semester>/')
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

@app.route('/Student/savefeedback/', methods = ['POST'])
def student_save_feedback():
	"""Save the feedback/issues given by the student in the database"""
	from University import Student, Student_feedback
	try:
		if request.method == 'POST':
			usn = request.form['usn'].lower()
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
	except:
		db.session.rollback()
		return "Cannot save feedback..."

@app.route('/Faculty/savefeedback/', methods = ['POST'])
def faculty_save_feedback():
	"""Save the feedback given by the faculty for a student in the database"""
	from University import Student, Faculty, Faculty_feedback
	try:
		if request.method == 'POST':
			fid = request.form['fid'].lower()
			student_usn = request.form['student_usn'].lower()
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
	except:
		db.session.rollback()
		return "Cannot save feedback..."


@app.route('/Student/login/', methods = ['POST'])
def student_login():
	from University import Student, Student_credential
	try:
		if request.method == 'POST':
			usn = request.form['usn'].lower()
			password = request.form['password']

			obj = Student_credential.query.filter(and_(Student_credential.usn == usn, Student_credential.password == password)).first()
			if obj != None:
				return "Sucess"
			else:
				return "Enter correct usn/password..."
	except:
		return "Error.."

@app.route('/Faculty/login/', methods = ['POST'])
def faculty_login():
	from University import Faculty, Faculty_credential
	try:
		if request.method == 'POST':
			fid = request.form['fid'].lower()
			password = request.form['password']

			obj = Faculty_credential.query.filter(and_(Faculty_credential.fid == fid , Faculty_credential.password == password)).first()
			if obj != None:
				#return redirect(url_for('faculty_home', fid = fid))
				return "Success.."
			else:
				return "Enter correct fid/password..."
	except:
		return "Error..."

@app.route('/Faculty/home/<int:fid>/')
def faculty_home(fid):
	from University import Student, Faculty, Student_and_advisor
	try:
		q = Student_and_advisor.query.filter_by(fid = fid).all()
		return render_template('facultyHomepage.html', advisors_students = q)
	except:
		pass