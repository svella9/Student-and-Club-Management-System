from flask import Flask, flash, request, abort, render_template
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

@app.route('/main/allocate')
def allocate_advisor():
	#Allocate students to each faculty satisying constraints such as:
	#	exactly 1 advisor per user
	#	no overlapping sems for advisor
	#	a faculty may not be advisor to any student"""
	students=Student.query.all()
	faculties=Faculty.query.all()
	#average no of students per faculty
	x=len(students)/len(faculties)
	#sem no,extra students per faculty for that sem
	sems={{1,0},{2,0},{3,0},{4,0},{5,0},{6,0},{7,0},{8,0}}
	#allocation list for each sem 0-not allocated  >1 no of faculty allocated <1 imdicates extra faculty required
	alloc={0,0,0,0,0,0,0,0}
	#indicates the number of extra faculty available
	spare=0;
	#max no of students a faculty can take over average no of students taken by faculty
	threshold=0.33
	#students saved so far
	extra=0
	run =0
	#second field denotes m/n ratio used to determing best sem to create spare
	sparelist=[[1,x],[2,x],[3,x],[4,x],[5,x],[6,x],[7,x],[8,x]]
    while len(sems)>0:
        for i in sems:
            semstud= Student.query.filter_by(sem = i).all()
            n=len(semstud)/x
            m=len(semstud)%x
            if m/n<(threshold*x):
                alloc[sems[i][0]]=n
                extra+=m
                if(extra>x):
                    extra-=x
                    spare+=1
                    del sems[i]
                    sparelist[sems[i][0]][1]=m/n
					#reduce the no of faculty required for sem if possible max spare required is 8 for 8 sems
            elif run<1:
                sems[i]=m/n
            elif run>=1:
                if(spare>0):
                    alloc[sems[i][0]]=n+1
                    spare-=1
                    del sems[i]
                else:	
                    #this sort is to use the sem with best chances of creating spare faculty
						#can be improved extra students/no of faculty cannot be the sole factor in determining best sem for reduction
						#checks only one sem for reduction...can be improved
                    sparelist.sort(key=lambda k: (-k[1]))
                    f=create_spare(sparelist[0][0],x,threshold)
                    alloc[sparelist[0][0]]-=f
                    alloc[sems[i][0]]=n+f
                    sparelist[0][1]*=((alloc[sparelist[0][0]]+f)/alloc[sparelist[0][0]])
                    del sems[i]
        #this sort is to address 1st in next run
        sems.sort(key=lambda k: (-k[1]))
        run+=1
		#actually distributing faculties
    for i in range(1,8):
		distribute(i,alloc)



def create_spare(i,x):
	semstud= Student.query.filter_by(sem = i).all()
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

def distribute(i,alloc):
	#alloc is the no of faculties allocated per sem
	n=alloc[i]
	semstud= Student.query.filter_by(sem = i).all()
	for j in range(0,alloc[i]):
		alist[j]=len(semstud)/n
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
	faculties=Faculty.query.filter_by(sem=-1).all()
	k=0
	for j in range(0,n-1):
        faculties[j].sem=i
		for b in range(1,alist[j]):
            semstud[k].advisor=faculties[j].name
            k+=1
	db.session.commit()

if __name__ == '__main__':
	app.run(debug = True)