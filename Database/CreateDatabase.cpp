#include <iostream>
#include <fstream>

using namespace std;

int main(){
    //this code os used to create a dummy databse for debugging
    ofstream myfile;
    myfile.open("FillUniversityData.sql");
    myfile<<"use University;"
    string insert_student="INSERT INTO student(usn,name,sem,dept,email,mob)";
    string insert_faculty="INSERT INTO student(fid,name,dept,email,mob,date,sem)"; 
    string exam_hall="INSERT INTO exam_hall(id,hallno,no_of_benches)";
    string faculty_credentials="INSERT INTO faculty_credential(fid,password)";
    string student_credentias="INSERT INTO student_credential(usn,password)";
    string faculty_subject_code="INSERT INTO faculty_subject_code(id,fid,scode)";
    string student_subject_code="INSERT INTO student_subject_code(id,usn,scode)";
    string branch_usn[]


}