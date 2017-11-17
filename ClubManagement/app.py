from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
#from database import *
#from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rakshith@localhost/clubmanagement' 
db = SQLAlchemy(app)

@app.route('/addNewClub')
def addNewClub():
	return render_template('clubInformation.html')

@app.route('/addClubToDatabase',methods = ['POST'])
def addClubToDatabase():
	from database import Club
	if request.method == 'POST':
		name = request.form['name']
		id = request.form['id']
		print(name)
		print()
		print()
		print(id)
		club = Club(name,id)
		print(club)
		db.session.add(club)
		db.session.commit()

		return 'Club Registered successfully!!'

	else:
		#Bad Request
		print(request.form['name'])
		abort(400)

@app.route('/addNewMember')
def addNewMember():
	return render_template('memberInformation.html')
  
@app.route('/Student/register', methods = ['POST'])
def student_register():
	from database import Member,Event_Volenteers,Attendance
	
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		
		member = Member(name,email)
		
		db.session.add(Member)
		db.session.commit()

		return 'Member added successfully!!'

	else:
		#Bad Request
		abort(400)
		
@app.route('/listAllMembers')
def list():
	return render_template("listAllMembers.html",member=Member.query.all())

@app.route('/addVolunterForAnEvent')
def addVolunterForAnEvent():
	return render_template('VolunterInformation.html')

@app.route('/addMemberToDatabase',methods = ['POST'])
def addMemberToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Member
	if request.method == 'POST':
		name = request.form['name']
		USN = request.form['USN']
		clubId = request.form['clubId']
		email = request.form['email']
		member=Member(clubId,name,USN,email)
		db.session.add(member)
		db.session.commit()

		return 'Member added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/markAttendanceOfAnEvent')
def markAttendanceOfAnEvent():
	return render_template('attendanceInformation.html')

@app.route('/markAttendanceToDatabase',methods = ['POST'])
def markAttendanceToDatabase():		
	from database import Member,Event,Event_Volenteers,Attendance
	
	if request.method == 'POST':
		name = request.form['name']
		eName = request.form['eventName']
		date = request.form['date']
		attendance=Attendance(name,ename,head)
		
		db.session.add(attendance)
		db.session.commit()

		return 'attendance added'
	else:
		#Bad Request
		abort(400)	
		
@app.route('/listAllVolunters')
def listAllVolunters():	
	return render_template("listAllVolunters.html",volenteer.query.all())	

@app.route('/listAllAttendance')
def listAllAttendance():
	return render_template("listAllVolunters.html",attendance.query.all())  

if __name__ == '__main__':
	app.run(debug=True)		
 
 