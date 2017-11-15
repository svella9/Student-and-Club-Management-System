from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
db = SQLAlchemy(app)

@app.route('/')
def index():
   return render_template('admin.html')


@app.route('/allotSeats/', methods =['POST', 'GET'])
def examination_seat_allotment():
    if request.method == 'POST':
        print(request.form.getlist('scode'))
        print(request.form.getlist('hallcode'))
        
        subject_code_list = request.form.getlist('scode')
        hall_code_list = request.form.getlist('hallcode')

        q1 = dict()
        q2 = dict()
        hall_capacity = dict()

        for scode in subject_code_list:
            q1[scode] = Student_subject_code.query.filter_by(scode = scode).all()
        
        for hallcode in Exam_hall:
            q2[hallcode] = Exam_hall.query.filter_by(hallcode = hallcode).first()
            hall_capacity[hallcode] = q2[hallocode].no_of_benches * 2
        
        total_students = 0
        total_hall_capacity = 0

        for key,value in q1.iteritems():
            total_students += len(value)
        for key, value in hall_capacity.iteritems():
            total_hall_capacity += value

        if total_students > total_hall_capacity:
            return "Number of students are more than the total capacity of the hall!!"
        
        #Algorithm for allocating students....
        




        return "Submit"

if __name__ == '__main__':
    app.run(debug = True,host="127.0.0.1",port=50001)