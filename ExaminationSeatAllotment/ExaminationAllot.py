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
        #print(request.form.getlist('scode'))
        #print(request.form.getlist('hallcode'))
        
        subject_code_list = request.form.getlist('scode')
        hall_code_list = request.form.getlist('hallcode')

        q1 = dict() #dictionary of subject code and list of students
        q2 = dict() #dictionary of hall code and capacity
        hall_capacity = dict()

        #get list of all students writing the exam and store it as key-value pair.
        for scode in subject_code_list:
            q1[scode] = Student_subject_code.query.filter_by(scode = scode).all()
        
        #get capacity of each hall and store it as a key value pair.
        for hallcode in Exam_hall:
            q2[hallcode] = Exam_hall.query.filter_by(hallcode = hallcode).first()
            hall_capacity[hallcode] = q2[hallocode].no_of_benches * 2
        
        total_students = 0
        total_hall_capacity = 0

        #find total students taking exam for that day
        for key,value in q1.iteritems():
            total_students += len(value)

        #find total capacity of all halls available on that day
        for key, value in hall_capacity.iteritems():
            total_hall_capacity += value

        if total_students > total_hall_capacity:
            return "Number of students are more than the total capacity of the hall!!"
        
        #Algorithm for allocating students....
        # Sort the subject code based on the number of students taking it.
        # Sort the halls based on the capacity
        # 

        sorted_q1 = sorted(q1, key = lambda x : len(q1[x])) #has subject code sorted in order of students taking it
        sorted_q2 = sorted(q2 , key = lambda x : q2[x].capacity) #hall code sorted in order of capcity
        hall_and_students = dict()

        list1 = []
        list2 = []

        for i in range(len(sorted_q1)):
            if i % 2 == 0:
                list1.extend(q1[sorted_q1[i]])
            else:
                list2.extend(q1[sorted_q1[i]])

        from itertools import zip_longest
        student_pair_list = list(zip_longest(list1, list2))
        #del list1, list2

        index = 0
        for hallcode in sorted_q2:
            hall_and_students[hallcode] = student_pair_list[index : index + q2[hallcode].capacity]
            index +=  q2[hallcode].capacity

        return render_template("seatingArrangement" , hall_and_students = hall_and_students)

if __name__ == '__main__':
    app.run(debug = True,host="127.0.0.1",port=50001)