from User import departmentlist
import pickle

class Course:
    __name = ""
    __code = ""
    __credit = 0
    __completion = "Remaining"

    __midClassTest = 0/5
    __mid = 0/40
    __finalClassTest = 0/5
    __final = 0/60
    __attendance = 0/5
    __assignment = 0/10
    __result = 0/100

    __teacher = ""
    __prerequisiteCode = "None"
    
    __time1 = ""
    __time2 = ""
    def __init__(self, code = "", name = "", credit = 0, prerequisiteCode = "None", time1 = "", time2 = ""):
        self.__code = code
        self.__name = name
        self.__credit = credit
        self.__prerequisiteCode = prerequisiteCode
        self.__time1 = time1
        self.__time2 = time2
    def setName(self, name):
        self.__name = name
    def setCode(self, code):
        self.__code = code
    def setCredit(self, credit):
        self.__credit = credit
    def setMidClassTest(self, score, outof = 100):
        self.__midClassTest = score
    def setMid(self, score, outof = 100):
        self.__mid = score
    def setFinalClassTest(self, score, outof = 100):
        self.__finalClassTest = score
    def setFinal(self, score, outof = 100):
        self.__final = score
    def setAttendance(self, score, outof = 100):
        self.__attendance = score
    def setAssignment(self, score, outof = 100):
        self.__assignment = score
    def setResult(self, result):
        self.__result = result
    def setTeacher(self, teacher):
        self.__teacher = teacher
    def setSemester(self, semester):
        self.__semester = semester
    def setPrerequisiteCode(self, code):
        self.__prerequisiteCode = code
    def setTime1(self, time1):
        self.__time1 = time1
    def setTime2(self, time2):
        self.__time2 = time2
    def markDone(self):
        self.__completion = "Done"
    def markCurrent(self):
        self.__completion = "Current"
    def markRemaining(self):
        self.__completion = "Remaining"
    def returnName(self):
        return self.__name
    def returnCode(self):
        return self.__code
    def returnCredit(self):
        return self.__credit
    def returnMidClassTest(self):
        return self.__midClassTest
    def returnMid(self):
        return self.__mid
    def returnFinalClassTest(self):
        return self.__finalClassTest
    def returnFinal(self):
        return self.__final
    def returnAttendance(self):
        return self.__attendance
    def returnAssignment(self):
        return self.__assignment
    def returnResult(self):
        return self.__result
    def returnTeacher(self):
        return self.__teacher
    def returnSemester(self):
        return self.__semester
    def returnPrerequisiteCode(self):
        return self.__prerequisiteCode
    def returnInfoShort(self):
        return [self.__code, str(self.__credit), self.__name]

daysoftheweek = ["SUN",  "MON",  "TUE",  "WED",  "THU",  "FRI",  "SAT"]
timesoftheday = ["8:30","10:00","11:30","13:00","14:30","16:00","17:30"]

class Routine:
    __courselist = {"SUN":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "MON":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "TUE":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "WED":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "THU":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "FRI":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None},
                    "SAT":{"8:30":None, "10:00":None, "11:30":None, "13:00":None, "14:30":None, "16:00":None, "17:30":None}}
    def __init__(self):
        for day in daysoftheweek:
            for time in timesoftheday:
                self.__courselist[day][time] = None
    def assignCourse(self, course = Course(), day = "", time = ""):
        self.__courselist[day][time] = course.returnCode()
    def clearSlot(self, day = "", time = ""):
        self.__courselist[day][time] = None

class CCSP:
    __courselist = {1: {}, 2: {}, 3: {},
                    4: {}, 5: {}, 6: {},
                    7: {}, 8: {}, 9: {},
                    10:{}, 11:{}, 12:{}}
    __department = ""
    def __init__(self, department):
        self.__department = department
    def returnDepartment(self):
        return self.__department
    def addCourse(self, semester, course_code, course = Course()):
        self.__courselist[semester][course_code] = course
    def removeCourse(self, semester, course_code, course = Course()):
        self.__courselist[semester][course_code] = course
    def viewSemester(self, semester):
        valuelist = []
        valuelist.append("Semester - " + str(semester))
        for course in self.__courselist[semester].values():
            valuelist.append("\t\t".join(course.returnInfoShort()))
        return valuelist
    def view(self, length = "full"):
        valuelist = []
        valuelist.append("CCSP of " + self.__department)
        if length == "full":
            for i in range(12):
                for course in self.viewSemester(i+1):
                    valuelist.append(course)
        elif length[:-2] == "semester":
            valuelist = self.viewSemester(length[-2:])
        return "\n".join(valuelist)
    def dump(self):
        with open(ccspfolder + self.__department + ".pkl", 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)

ccsplist = dict((d, CCSP(d)) for d in departmentlist.keys())

ccspfolder = "Database/CCSP/"




