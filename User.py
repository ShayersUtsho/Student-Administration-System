import datetime as dt
import pickle

def generateID(department, transferSemester=1):
    date = dt.datetime.now()
    idYear = "".join(list(date.strftime("%Y"))[2:])
    idSession = str(1+(int(date.strftime("%m"))-1)//4)
    deptno = departmentlist[department]
    semester = str(transferSemester)
    rollKey = idYear + idSession + deptno + semester
    if int(rollKey) in list(roll.keys()):
        roll[int(rollKey)] += 1
    else:
        roll[int(rollKey)] = 1
    rollno = "0"*(3-len(str(roll[int(rollKey)])))+str(roll[int(rollKey)])
    return idYear + idSession + deptno + semester + rollno

class User:
    _username = ""
    _password = ""
    def __init__(self, username="", password="00000000"):
        self._username = username
        self._password = password
    def create(self, username, password="00000000"):
        self._username = username
        self._password = password
    def checkUsername(self, username):
        return self._username == username
    def checkPassword(self, password):
        return self._password == password
    def changePassword(self, password):
        self._password = password
    def returnUsername(self):
        return self._username
    def returnPassword(self):
        return self._password
    def returnFull(self):
        return {"Username":self._username, "Password":self._password}

class Student(User):
    #admission information
    _name = ""
    _DoB = dt.datetime(2000, 1, 1)
    _fathersName = ""
    _mothersName = ""
    _email = ""
    _phoneNo = ""
    _address = ""
    _SSC = 0
    _HSC = 0
    _reference = User()
    #understudy information
    _id = ""
    _semester = 1
    _department = ""
    _batch = 1
    
    
    def __init__(self, username="", password="00000000", department = "", semester = 1):
        super().__init__(username, password)
        self._id = self._username
        self._department = department
        self._semester = semester
    def setSemester(self, semester = 1):
        self._semester = semester
    def setDepartment(self, department):
        self._department = department
    def setBatch(self, batch):
        self._batch = batch
    def setName(self, name):
        self._name = name
    def setDoB(self, year, month, day):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self._DoB = dt.datetime(self.year, self.month, self.day)
    def setFathersName(self, fathers_name):
        self._fathersName = fathers_name
    def setMothersName(self, mothers_name):
        self._mothersName = mothers_name
    def setEmail(self, email):
        self._email = email
    def setPhoneNo(self, phone_no):
        self._phoneNo = phone_no
    def setAddress(self, address):
        self._address = address
    def setSSC(self, gpa):
        self._SSC = float(gpa)
    def setHSC(self, gpa):
        self._HSC = float(gpa)
    def setReference(self, idno):
        self._reference = Student(idno)
    def returnInfoShort(self):
        return [self._id, self._name, self._department, str(self._batch), str(self._semester)]
    def returnInfoLong(self):
        valuelist = []
        valuelist.append("Student ID")
        valuelist.append(self._id)
        valuelist.append("Semester")
        valuelist.append(str(self._semester))
        valuelist.append("Department")
        valuelist.append(self._department)
        valuelist.append("Batch")
        valuelist.append(str(self._batch))
        valuelist.append("Name")
        valuelist.append(self._name)
        valuelist.append("Date of Birth")
        valuelist.append(self._DoB.strftime("%x"))
        valuelist.append("Father's Name")
        valuelist.append(self._fathersName)
        valuelist.append("Mother's Name")
        valuelist.append(self._mothersName)
        valuelist.append("Email")
        valuelist.append(self._email)
        valuelist.append("Phone No.")
        valuelist.append(self._phoneNo)
        valuelist.append("Address")
        valuelist.append(self._address)
        valuelist.append("SSC:")
        valuelist.append(str(self._SSC))
        valuelist.append("HSC:")
        valuelist.append(str(self._HSC))
        valuelist.append("Reference")
        valuelist.append(self._reference.returnID())
        return valuelist
    def returnDepartment(self):
        return self._department
    def returnID(self):
        return self._id
    def dump(self):
        with open(studentFolder + self._id + ".pkl", 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)

class Teacher(User):
    _name = ""
    _phoneNo = ""
    _email = ""
    _address = ""
    _honors = 0
    _masters = 0
    _department = ""
    hod = False
    def __init__(self, username="", department = "", password="00000000"):
        super().__init__(username, password)
        self._username = self._username
        self._department = department
    def setName(self, name):
        self._name = name
    def setPhoneNo(self, phoneNo):
        self._phoneNo = phoneNo
    def setEmail(self, email):
        self._email = email
    def setAddress(self, address):
        self._address = address
    def setHonors(self, honors):
        self._honors = honors
    def setMasters(self, masters):
        self._masters = masters
    def setDepartment(self, department):
        self._department = department
    def setHoD(self):
        self.hod = True
    def unsetHoD(self):
        self.hod = False
    def returnName(self):
        return self._name
    def returnPhoneNo(self):
        return self._phoneNo
    def returnEmail(self):
        return self._email
    def returnAddress(self):
        return self._address
    def returnHonors(self):
        return self._honors
    def returnMasters(self):
        return self._masters
    def returnDepartment(self):
        return self._department
    def checkHoD(self):
        return self.hod
    def returnInfoShort(self):
        return [self._department, self._name]
    def returnInfoLong(self):
        valuelist = []
        valuelist.append("Name:")
        valuelist.append(self._name)
        valuelist.append("Phone No.:")
        valuelist.append(self._phoneNo)
        valuelist.append("Email:")
        valuelist.append(self._email)
        valuelist.append("Address:")
        valuelist.append(self._address)
        valuelist.append("Honors CGPA:")
        valuelist.append(self._honors)
        valuelist.append("Masters CGPA:")
        valuelist.append(self._masters)
        valuelist.append("Department:")
        valuelist.append(self._department)
        return valuelist
    def dump(self):
        with open(teacherFolder + self._username + ".pkl", 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)

class HeadOfDepartment(Teacher):
    hod = True
    def dump(self):
        with open(hodFolder + self._username + ".pkl", 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)
    def returnInfoShort(self):
        return [self._department, self._name]
    def returnInfoLong(self):
        valuelist = []
        valuelist.append("Name:")
        valuelist.append(self._name)
        valuelist.append("Phone No.:")
        valuelist.append(self._phoneNo)
        valuelist.append("Email:")
        valuelist.append(self._email)
        valuelist.append("Address:")
        valuelist.append(self._address)
        valuelist.append("Honors CGPA:")
        valuelist.append(self._honors)
        valuelist.append("Masters CGPA:")
        valuelist.append(self._masters)
        valuelist.append("Department:")
        valuelist.append(self._department)
        return valuelist

class Admin(User):
    pass

class AdmissionOffice(User):
    pass

class AccountsOffice(User):
    pass

roll = {}
studentlist = {}
teacherlist = {}
hodlist = {}

studentFolder = "Database/Students/"
teacherFolder = "Database/Teachers/"
hodFolder = "Database/HoD/"

departmentlist = {"FDT" :"01",
                  "IA"  :"02",
                  "GDM" :"03",
                  "AMMT":"05",
                  "CSIT":"06",
                  "CSE" :"07",
                  "BBA" :"40"
                  }

admin = Admin("admin", "1234abcD")
specialAccessUserList = {"admission":AdmissionOffice("admission", "2314bcaD"),
                         "accounts":AccountsOffice("accounts", "4321dcbA")}











