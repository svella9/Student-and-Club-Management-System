from flask import Flask, flash, request, redirect, abort, render_template, session, url_for
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
			usn = request.form['usn'].upper()
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
			fid = request.form['fid'].upper()
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


@app.route('/admin/notify/', methods = ['POST'])
def send_notification():
	"""Send notification to all students belonging to a particular semester"""
	from University import Student, Faculty
	try:
		if request.method == 'POST':
			date = request.form['date']
			semester = request.form['semester']

			#query to retrieve students
			students = Student.query.filter_by(sem = semester).all()
			faculties = Faculty.query.all()
			#keep only the email-id of the students
			students = list(map(lambda x : x.email, students))
			faculties = list(map(lambda x: x.email, faculties))
			print('sending Message', students)
			msg = Message('Meeting Schedule Notification.',
					sender = 'pesfacultyadvisor.sepro2017@gmail.com',
					recipients = students , cc = faculties)
			#print('Object created!')
			msg.body = "Dear Student\n A meeting is scheduled on " + date + ".\n We request you to meet your faculty advisor."
			mail.send(msg)

			return "Notification Sent!!"

	except Exception as e:
		print(e)
		return "Something went wrong. Please check your internet connection.."


@app.route('/Student/savefeedback/', methods = ['POST'])
def student_save_feedback():
	"""Save the feedback/issues given by the student in the database"""
	from University import Student, Student_feedback
	try:
		if request.method == 'POST':
			usn = request.form['usn'].upper()
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
			fid = request.form['fid'].upper()
			student_usn = request.form['usn'].upper()
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
	except Exception as e:
		print(e)
		db.session.rollback()
		return "Cannot save feedback..."

@app.route('/Student/login/', methods = ['POST'])
def student_login():
	from University import Student, Student_credential
	try:
		if request.method == 'POST':
			usn = request.form['usn']
			password = request.form['password']
			obj = Student_credential.query.filter(and_(Student_credential.usn == usn, Student_credential.password == password)).first()
			if obj != None:
				session['usn'] = usn
				#return "Sucess"
				return redirect(url_for('student_home'))
			else:
				return "Enter correct usn/password..."
	except Exception as e:
		print(e)
		return "Error.."


@app.route('/Student/logout/')
def student_logout():
	#remove the usn from the session
	session.pop('usn', None)
	return redirect(url_for('getStudentLogin'))


@app.route('/Faculty/login/', methods = ['POST'])
def faculty_login():
	from University import Faculty, Faculty_credential
	try:
		if request.method == 'POST':
			fid = request.form['fid'].upper()
			password = request.form['password']

			obj = Faculty_credential.query.filter(and_(Faculty_credential.fid == fid , Faculty_credential.password == password)).first()
			if obj != None:
				#return redirect(url_for('faculty_home', fid = fid))
				session['fid'] = fid
				#print(session['fid'])
				#return "Success.."
				return redirect(url_for('faculty_home'))
			else:
				return "Enter correct fid/password..."
	except Exception as e:
		print(e)
		return "Error..."


@app.route('/Faculty/logout/')
def faculty_logout():
	#remove the fid from the session
	print('faculty logout')
	session.pop('fid', None)
	print('fid' in session)
	return redirect(url_for('getFacultyLogin'))


@app.route('/Faculty/home/')
def faculty_home():
	from University import Student, Faculty, Student_and_advisor
	try:
		#return "Success"
		if 'fid' in session:
			fid = session['fid']
			fobj = Faculty.query.filter_by(fid = fid).first()
			q = Student_and_advisor.query.filter_by(fid = fid).all()
			#print(q[0].student.name)
			return render_template('facultyHomepage.html', advisor = fobj, advisors_students = q)
		else:
			print('Please login')
			return redirect(url_for('getFacultyLogin'))
	
	except Exception as e:
		print(e)
		return "Error..."


@app.route('/Student/home/')
def student_home():
	"""Render Student homepage with advisor details, his feedbacks and a form to submit new feedback"""
	from University import Student, Student_feedback, Student_and_advisor, Faculty
	try:
		if 'usn' in session:
			usn = session['usn']
			sobj = Student.query.filter_by(usn = usn).first()
			fobj = Student_and_advisor.query.filter_by(usn = usn).first()
			if fobj != None:
				fobj = Faculty.query.filter_by(fid = fobj.fid).first()
			q = Student_feedback.query.filter_by(usn = usn).all()
			return render_template('studentHomepage.html', student = sobj, advisor = fobj, feedbacks = q)
		else:
			print('Please login')
			return redirect(url_for('getStudentLogin'))

	except Exception as e:
		print(e)
		return "Error..."

@app.route('/Faculty/giveFeedback/<usn>/')
def get_faculty_feedback_page(usn):
	"""Provide a interface for the advisor to view or to give feedback for the students"""
	from University import Student, Faculty, Faculty_feedback, Student_feedback, Student_and_advisor
	try:
		if 'fid' in session:
			fid = session['fid']
			sobj = Student.query.filter_by(usn = usn).first()
			fobj = Student_and_advisor.query.filter_by(usn = usn).first()
			q = Faculty_feedback.query.filter(and_(Faculty_feedback.fid == fid, Faculty_feedback.student_usn == usn)).all()
			stud_q = Student_feedback.query.filter_by(usn = usn).all()
			return render_template('feedbackByFaculty.html', student = sobj, advisor = fobj, feedbacks = q, student_feedbacks = stud_q)
		else:
			print('Please Login')
			return redirect(url_for('getFacultyLogin'))
	except Exception as e:
		print(e)
		return "Error..."


@app.route('/admin/')
def getAdminLogin():
	return render_template('adminlogin.html')


@app.route('/admin/login/', methods = ['POST'])
def admin_login():
	"""Process Admin login credentials"""
	from University import Faculty_credential
	try:
		if request.method == 'POST':
			password = request.form['password']
			obj = Faculty_credential.query.filter(and_(Faculty_credential.fid == "admin2017" , Faculty_credential.password == password)).first()
			if obj != None:
				#return redirect(url_for('faculty_home', fid = fid))
				session['fid'] = "admin2017"
				#return "Success.."
				return redirect(url_for('admin_home'))
			else:
				return "Incorrect password..."
	except Exception as e:
		print(e)
		return "Error..."


@app.route('/admin/logout/')
def admin_logout():
	session.pop('fid', None)
	return redirect(url_for('getAdminLogin'))

@app.route('/admin/home/')
def admin_home():
	if 'fid' in session and session['fid'] == 'admin2017':
		#return "Admin login success"
		return render_template('adminHomepage.html')
	else:
		return "Please go back and Login as admin..."





#Sathkrith code

@app.route('/main/allocate')
def allocate_advisor():
	from University import Student, Faculty, Student_and_advisor
	dept=["CSE","ISE","EEE","ECE","MEE","BTE","CVE"]
	for dep in dept:
		students=Student.query.filter_by(dept=dep).all()
		faculties=Faculty.query.filter_by(dept=dep).all()
		#average no of students per faculty
		print(len(students),len(faculties))
		x=len(students)//len(faculties)
		#sem no,extra students per faculty for that sem
		sems=[[1,0],[3,0],[5,0],[7,0]]
		#allocation list for each sem 0-not allocated  >1 no of faculty allocated <1 imdicates extra faculty required
		alloc=[0,0,0,0,0,0,0,0]
		#indicates the number of extra faculty available
		spare=0
		#max no of students a faculty can take over average no of students taken by faculty
		threshold=0.33
		#students saved so far
		extra=0
		run =0
		#second field denotes m/n ratio used to determing best sem to create spare
		sparelist=[[1,x],[3,x],[5,x],[7,x]]
		print(x)
		while(len(sems)>0):
			for i in sems:
				semstud= Student.query.filter(and_(Student.sem == i[0], Student.dept == dep)).all()
				#print(len(semstud),"x:",x)
				n=len(semstud)//x
				m=len(semstud)%x
				print(n,m)
				if m/n<(threshold*x):
					alloc[i[0]]=n
					extra+=m
					if(extra>x):
						extra-=x
						spare+=1
						for j in sparelist:
							if(i[0] == j[0]):
								j[1] = m/n
					sems.pop(sems.index(i))
						#reduce the no of faculty required for sem if possible max spare required is 8 for 8 sems sems.pop(sem.index(i))
				elif run<1:
					i[1]=m/n
				elif run>=1:
						if(spare>0):
							alloc[i[0]]=n+1
							spare-=1
							sems.pop(sems.index(i))
						else :
							#this sort is to use the sem with best chances of creating spare faculty
							#can be improved extra students/no of faculty cannot be the sole factor in determining best sem for reduction
							#checks only one sem for reduction...can be improved
							sparelist.sort(key=lambda k: (-k[1]))
							f=create_spare(sparelist[0][0],x,threshold,dep)
							alloc[sparelist[0][0]]-=f
							alloc[i[0]]=n+f
							sparelist[0][1]*=((alloc[sparelist[0][0]]+f)/alloc[sparelist[0][0]])
							sems.pop(sems.index(i))
				#this sort is to address 1st in next run
			print("done")
			sems.sort(key=lambda k: (-k[1]))
			run+=1
				#actually distributing faculties
		for i in range(1,8,2):
			distribute(i,alloc,dep)
	return "Allocation done successfully!"

def create_spare(i,x,threshold,dep):
	from University import Student, Faculty, Student_and_advisor
	semstud= Student.query.filter(and_(Student.sem == i, Student.dept == dep)).all()
	n=len(semstud)/x
	m=len(semstud)%x
	x=x+x*threshold
	#using max no of stud per faculty
	n1=len(semstud)/x
	m1=len(semstud)%x
	if n1<n:
		return 1
	else:
		return 0

def distribute(i,alloc,dep):
	from University import Student, Faculty, Student_and_advisor
	#alloc is the no of faculties allocated per sem
	n=alloc[i]
	semstud= Student.query.filter(and_(Student.sem == i, Student.dept == dep)).all()
	alist=[]
	for j in range(0,alloc[i]):
		alist.append(len(semstud)//n)
	m=len(semstud)%n
	k=0
	#alist contains exact no of students per faculty
	while(m):
		alist[k]+=1
		m-=1
		if k+1>n:
			k=0
		else:
			k+=1
	#sem =-1 indicates that faculty has not been assigned to any sem
	#proposed: improve the algo by assigning experienced lecturers to students in later sem

	faculties=Faculty.query.filter_by(dept=dep).all()
	k=0
	for j in range(0,n):
		for b in range(1,alist[j]+1):
			student_adv= Student_and_advisor(semstud[k].usn,faculties[j].fid, semstud[k], faculties[j])
			db.session.add(student_adv)
			k+=1
	db.session.commit()