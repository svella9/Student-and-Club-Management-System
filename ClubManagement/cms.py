from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ' ' 
db = SQLAlchemy(app)

@app.route('/addNewMember')
def addNewMember():
  return render_template('memberInformation.html')
  
@app.route('/Student/register', methods = ['POST'])
def student_register():
	from Clubmanagement import Member,Event,Event_Volenteers,Attendance
	
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

@app.route('/addVolunterToDatabase',methods = ['POST'])
def addVolunterToDatabase():  
    from Clubmanagement import Member,Event,Event_Volenteers,Attendance
	
	if request.method == 'POST':
		name = request.form['name']
		head = request.form['head']
		
		volenteer=Event_Volenteers(name,head)
		
		db.session.add(volenteer)
        db.session.commit()

		return 'volenteer added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/markAttendanceOfAnEvent')
def markAttendanceOfAnEvent():
  return render_template('attendanceInformation.html')

@app.route('/markAttendanceToDatabase',methods = ['POST'])
def markAttendanceToDatabase():		
    from Clubmanagement import Member,Event,Event_Volenteers,Attendance
	
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
 
 