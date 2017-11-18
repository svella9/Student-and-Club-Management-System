#include<iostream>
#include<fstream>
#include<cstdlib>
#include<string>
using namespace std;

int main() {
	ofstream myfile;
	myfile.open("Exam.sql");
	int i,j,k;
	string insertHall="INSERT INTO exam_hall(id,hallno,no_of_benches)";
	string insertDept="INSERT INTO dept_subject_code(id,dept,scode)";
	string insertScode="INSERT INTO student_subject_code(usn,scode)";
	string dept[8]={"CSE","ISE","MEE","EEE","ECE","BTE","CVE"};
	string usn = "1PI";
	string name = "";
	string query = "";
	int usnSem = 14;
	int sem = 7;
	string hall="";
	string code="CSE20";
	myfile<<"use exam;"<<endl;
	for(i=0;i<3;i++){
		code+=to_string(i);
		for(j=0;j<100;j++){
			query = insertScode + " VALUES(\"" + to_string((i+1)*100+j) + "\",\""+code+"\");";
			myfile<<query<<endl;

		}
		code="CSE20";
	}
	for(i=0;i<7;i++){
		for(j=0;j<3;j++){
			for(k=0;k<4;k++){
			hall=(char)((int)'A'+i);
			hall+=to_string(100*(j+1)+k);
			query = insertHall + " VALUES("+to_string(12*i+j*3+k)+",\"" + hall + "\","+to_string(30)+");";
			//myfile<<query<<endl;	
			}
		}

	}
	for(i=0;i<7;i++){
	sem=1;
	for(j=0;j<6;j++){
		query=insertDept+" Values(\""+dept[i]+"\",\""+"PI"+to_string(sem*100+j)+"\");";
        			//myfile<<query<<endl;	

	}
	for(sem=2;sem<=4;sem++){
		for(j=0;j<6;j++){
		query=insertDept+" Values(\""+dept[i]+"\",\""+dept[i]+to_string(sem*100+j)+"\");";
        		//	myfile<<query<<endl;	

	}
	}
	for(sem=4;sem<=8;sem++){
		for(j=0;j<12;j++){
		query=insertDept+" Values(\""+dept[i]+"\",\""+dept[i]+to_string(sem*100+j)+"\");";
        			//myfile<<query<<endl;	

		}
	}
	}

    return 0;
}