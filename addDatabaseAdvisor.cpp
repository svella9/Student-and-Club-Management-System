#include<iostream>
#include<fstream>
#include<cstdlib>
#include<string>
using namespace std;

int main() {
	ofstream myfile;
	myfile.open("faculty.sql");
	int i,j,k;
	string insertStudents = "INSERT INTO student(usn,name,sem,dept,email,mob)";
	string insertStudentCredential="INSERT INTO student_credential(usn,password)";
	string insertFacultyCredential="INSERT INTO faculty_credential(fid,password)";
	string insertFaculty = "INSERT INTO faculty(fid,name,dept,email,mob)";
	string insertHall="INSERT INTO exam_hall(id,hallno,no_of_benches)";
	string insertDept="INSERT INTO dept_subject_code(dept,scode)";
	string dept[8]={"CSE","ISE","MEE","EEE","ECE","BTE","CVE"};
	string usn = "1PI";
	string name = "";
	string query = "";
	string query2="";
	int usnSem = 14;
	int sem = 7;
	myfile<<"use University;";
	for(k=0;k<7;k++){
		for (int sem = 7; sem >= 1; sem -= 2) {
			usn = usn + to_string(usnSem + (7 - sem))+dept[k];
			for (int i = 0; i < 100; i++) {
				name = "";
				query = "";
				for (int j = 0; j < 5; j++) {
					name += (char)((int)'a' + rand() % 26);

				}
				query = insertStudents + " VALUES(\"" + usn + to_string(i) + "\",\"" + name + "\"," + to_string(sem) + ",\""+dept[k]+"\",\"" + name + "@gmail.com\",93938"+to_string(k) + to_string(sem * 100 + i) + ");";
				query2=insertStudentCredential+ "VALUES(\""+usn+to_string(i)+"\",\""+usn+to_string(i)+"\");";
				myfile << query<<endl;
				myfile<<query2<<endl;


			}
			usn = "1PI";
		}
	}
	sem = 7;
	for(k=0;k<7;k++){
	for (int sem = 7; sem >= 1; sem -= 2) {
		usn =dept[k]+to_string(sem);
		for (int i = 0; i < 7; i++) {
			name = "";
			query = "";
			for (int j = 0; j < 5; j++) {
				name += (char)((int)'a' + rand() % 26);

			}
			query = insertFaculty + " VALUES(\"" + usn + to_string(i) + "\",\"" + name + "\",\""+dept[k]+"\",\"" + name + "@gmail.com\",93938"+to_string(k) + to_string(sem * 20 + i) + ");";
			query2=insertFacultyCredential+ "VALUES(\""+usn+to_string(i)+"\",\""+usn+to_string(i)+"\");";
			myfile << query << endl;
			myfile<<query2<<endl;

		}
	}
	}

}
