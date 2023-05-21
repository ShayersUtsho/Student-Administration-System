import tkinter as tk
from os import listdir
from os.path import isfile, join
import pickle

from User import Student, Teacher, HeadOfDepartment
from User import departmentlist, studentlist, teacherlist, hodlist, admin, specialAccessUserList, studentFolder, teacherFolder, hodFolder
from User import generateID
from Course import Course, Routine, CCSP
from Course import ccsplist, ccspfolder

color = {"background":{}, "foreground":{}, "activebackground":{}, "activeforeground":{}, "set":{}}
color["background"]["window"] = "#06032c"
color["background"]["label"] = "#06032c"
color["foreground"]["label"] = "#f0f0f0"
color["background"]["entry"] = "white"
color["foreground"]["entry"] = "#0c075e"
color["background"]["radio"] = "#06032c"
color["foreground"]["radio"] = "#f0f0f0"
color["activebackground"]["radio"] = "#0c075e"
color["activeforeground"]["radio"] = "white"
color["set"]["radio"] = "black"
color["background"]["button"] = "#0c075e"
color["foreground"]["button"] = "white"
color["activebackground"]["button"] = "#06032c"
color["activeforeground"]["button"] = "#f0f0f0"

class App(tk.Tk):
    page = {}
    active_page = ""
    option = ""
    i=10
    chk = False
    def __init__(self):
        super().__init__()

        self.refreshStudentsList()
        self.refreshTeachersList()
        self.refreshHoDList()
        self.refreshCCSPList()

        self.admissionNeedsBackButton = True
        self.viewTeacherNeedsBackButton = True
        self.viewHoDNeedsBackButton = True
        self.option = tk.StringVar(master = self, value="student")
        self.modifyingID = ""
        self.teacherToBeModified = ""
        self.loggedUsername = ""
        self.loggedAccountType = ""
        self.loggedDeparment = ""
        
        self.active_page = "login"
        
        self.title("SMUCT Student Administration System")
        self.geometry("600x600+700+300")
        self.configure(bg=color["background"]["window"])
        
        self.page["login"] = {}
        self.page["login"]["title"] = tk.Label(self,                                                                            font=100,   bg=color["background"]["label"], fg=color["foreground"]["label"], text = "Welcome to SMUCT portal")
        self.page["login"]["instructions"] = tk.Label(self, text = "Please select your user-type",                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["login"]["option1"] = tk.Radiobutton(self, text = "Student", variable=self.option, value="student",                       bg=color["background"]["radio"], fg=color["foreground"]["radio"], activebackground=color["activebackground"]["radio"], activeforeground=color["activeforeground"]["radio"], selectcolor=color["set"]["radio"])
        self.page["login"]["option2"] = tk.Radiobutton(self, text = "Teacher", variable=self.option, value="teacher",                       bg=color["background"]["radio"], fg=color["foreground"]["radio"], activebackground=color["activebackground"]["radio"], activeforeground=color["activeforeground"]["radio"], selectcolor=color["set"]["radio"])
        self.page["login"]["option3"] = tk.Radiobutton(self, text = "Head of Department", variable=self.option, value="hod",                bg=color["background"]["radio"], fg=color["foreground"]["radio"], activebackground=color["activebackground"]["radio"], activeforeground=color["activeforeground"]["radio"], selectcolor=color["set"]["radio"])
        self.page["login"]["option4"] = tk.Radiobutton(self, text = "Administrative", variable=self.option, value="administrative",         bg=color["background"]["radio"], fg=color["foreground"]["radio"], activebackground=color["activebackground"]["radio"], activeforeground=color["activeforeground"]["radio"], selectcolor=color["set"]["radio"])
        self.page["login"]["username label"] = tk.Label(self, text = "Username",                                                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["login"]["username"] = tk.Entry(self,                                                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["login"]["password label"] = tk.Label(self, text = "Password",                                                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["login"]["password"] = tk.Entry(self, show="*",                                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["login"]["loginbutton"] = tk.Button(self, text = "Login", command=self.login,                                             bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"], width=12)
        
        self.page["student"] = {}
        self.page["student"]["title"] = tk.Label(self,                                                                                      bg=color["background"]["label"], fg=color["foreground"]["label"], text = "Please select an action")
        self.page["student"]["button1"] = tk.Button(self, text = "View CCSP", command=self.studentviewCCSP,                                        bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["student"]["button2"] = tk.Button(self, text = "Select Course", command=self.selectCourse,                                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["student"]["button3"] = tk.Button(self, text = "View Courses", command=self.viewCourses,                                  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["student"]["button4"] = tk.Button(self, text = "View Routine", command=self.viewRoutine,                                  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["student"]["button5"] = tk.Button(self, text = "Change Account Password", command=lambda:self.changePassword("student"),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["student"]["button6"] = tk.Button(self, text = "Logout", command=lambda:self.packAll("login"),                            bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["student"].values():
            button.configure(width=20)
        
        self.page["teacher"] = {}
        self.page["teacher"]["title"] = tk.Label(self, text = "Please select an action",                                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["teacher"]["button1"] = tk.Button(self, text = "View Courses", command=self.viewCourses,                                  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["teacher"]["button2"] = tk.Button(self, text = "View Routine", command=self.viewRoutine,                                  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["teacher"]["button3"] = tk.Button(self, text = "Change Account Password", command=lambda:self.changePassword("teacher"),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["teacher"]["button4"] = tk.Button(self, text = "Logout", command=lambda:self.packAll("login"),                            bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["teacher"].values():
            button.configure(width=20)
        
        self.page["hod"] = {}
        self.page["hod"]["title"] = tk.Label(self, text = "Please select an action",                                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["hod"]["button1"] = tk.Button(self, text = "CCSP Management", command=self.ccspManagement,                                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod"]["button2"] = tk.Button(self, text = "Student Management", command=self.studentManagement,                          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod"]["button3"] = tk.Button(self, text = "Teacher Management", command=self.teacherManagement,                          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod"]["button4"] = tk.Button(self, text = "Routine Management", command=self.routineManagement,                          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod"]["button5"] = tk.Button(self, text = "Change Account Password", command=lambda:self.changePassword("hod"),          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod"]["button6"] = tk.Button(self, text = "Logout", command=lambda:self.packAll("login"),                                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["hod"].values():
            button.configure(width=20)
        
        self.page["CCSP Management"] = {}
        self.page["CCSP Management"]["title"] = tk.Label(self, text = "Please select an action",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["semester label"] = tk.Label(self, text = "Semester",                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["semester"] = tk.Entry(self,                                                                   bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["CCSP Management"]["course code label"] = tk.Label(self, text = "Course Code",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["course code"] = tk.Entry(self,                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["CCSP Management"]["course name label"] = tk.Label(self, text = "Course Name",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["course name"] = tk.Entry(self,                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["CCSP Management"]["course credit label"] = tk.Label(self, text = "Credit",                                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["course credit"] = tk.Entry(self,                                                              bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["CCSP Management"]["prerequisite code label"] = tk.Label(self, text = "Pre-requisite Code",                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["CCSP Management"]["prerequisite code"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=15)
        self.page["CCSP Management"]["button2"] = tk.Button(self, text = "Add Course", command=self.addCourseToCCSP,                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["CCSP Management"]["button3"] = tk.Button(self, text = "Remove Course", command=self.removeCourseFromCCSP,        bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["CCSP Management"]["button5"] = tk.Button(self, text = "Back", command=lambda:self.packAll("hod"),                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["CCSP Management"]["ccsp"] = tk.Message(self, text = "",                                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        
        self.page["Student Management"] = {}
        self.page["Student Management"]["title"] = tk.Label(self, text = "Please select an action",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Student Management"]["button1"] = tk.Button(self, text = "View Students", command=self.ccspManagement,           bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student Management"]["button2"] = tk.Button(self, text = "View Course Requests", command=self.ccspManagement,    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student Management"]["button3"] = tk.Button(self, text = "Edit Course Requests", command=self.ccspManagement,    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student Management"]["button4"] = tk.Button(self, text = "Approve Course Requests", command=self.ccspManagement, bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student Management"]["button5"] = tk.Button(self, text = "Back", command=self.ccspManagement,                    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["Student Management"].values():
            button.configure(width=20)
        
        self.page["Teacher Management"] = {}
        self.page["Teacher Management"]["title"] = tk.Label(self, text = "Please select an action",                                bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Teacher Management"]["button1"] = tk.Button(self, text = "View Teachers", command=self.ccspManagement,          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Management"]["button2"] = tk.Button(self, text = "View Assigned Courses", command=self.ccspManagement,  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Management"]["button3"] = tk.Button(self, text = "Assign Course", command=self.ccspManagement,          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Management"]["button4"] = tk.Button(self, text = "De-assign Course", command=self.ccspManagement,       bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Management"]["button5"] = tk.Button(self, text = "Back", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["Teacher Management"].values():
            button.configure(width=20)
        
        self.page["Routine Management"] = {}
        self.page["Routine Management"]["title"] = tk.Label(self, text = "Please select an action",                                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Routine Management"]["button1"] = tk.Button(self, text = "View Routine", command=self.ccspManagement,                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Routine Management"]["button2"] = tk.Button(self, text = "View CCSP", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Routine Management"]["button3"] = tk.Button(self, text = "View CCSP", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Routine Management"]["button4"] = tk.Button(self, text = "View CCSP", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Routine Management"]["button5"] = tk.Button(self, text = "View CCSP", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Routine Management"]["button6"] = tk.Button(self, text = "View CCSP", command=self.ccspManagement,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["Routine Management"].values():
            button.configure(width=20)

        self.page["admin"] = {}
        self.page["admin"]["title"] = tk.Label(self, text = "Please select a system",                                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["admin"]["button1"] = tk.Button(self, text = "Special Access Users", command=self.openSpecialAccessUserPanel,     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admin"]["button2"] = tk.Button(self, text = "Academics", command=self.openAdminsAcademics,                       bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admin"]["button3"] = tk.Button(self, text = "Account System", command=self.openAdminsAccountSystem,              bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admin"]["button4"] = tk.Button(self, text = "Teacher Profiles", command=self.openAdminsTeacherProfile,           bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admin"]["button5"] = tk.Button(self, text = "HoD Profiles", command=self.openAdminsHoDProfile,                   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admin"]["button6"] = tk.Button(self, text = "Log Out", command=self.logout,                                      bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["admin"].values():
            button.configure(width=20)

        self.page["Special Access Users"] = {}
        self.page["Special Access Users"]["heading1"] = tk.Label(self, text = "Username",                                                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["heading2"] = tk.Label(self, text = "Password",                                                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["admission username"] = tk.Label(self, text = specialAccessUserList["admission"].returnUsername(),            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["admission password"] = tk.Label(self, text = specialAccessUserList["admission"].returnPassword(),            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["admission password new"] = tk.Entry(self,                                                                    bg=color["background"]["entry"], fg=color["foreground"]["entry"], width=20)
        self.page["Special Access Users"]["change admission password"] = tk.Button(self, text = "Change", command=self.changeAdmissionPassword,         bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Special Access Users"]["accounts username"] = tk.Label(self, text = specialAccessUserList["accounts"].returnUsername(),              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["accounts password"] = tk.Label(self, text = specialAccessUserList["accounts"].returnPassword(),              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Special Access Users"]["accounts password new"] = tk.Entry(self, width=20,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Special Access Users"]["change accounts password"] = tk.Button(self, text = "Change", command=self.changeAccountsPassword,           bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Special Access Users"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admin"),                                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["Teacher Profiles"] = {}
        self.page["Teacher Profiles"]["title"] = tk.Label(self, text = "Please select an action",                                           bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Teacher Profiles"]["button1"] = tk.Button(self, text = "Register New Teacher", command=self.registerNewTeacher,          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Profiles"]["button2"] = tk.Button(self, text = "View Teacher List", command=self.viewTeacherList,                bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher Profiles"]["button3"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admin"),                     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["Teacher Profiles"].values():
            button.configure(width=20)

        self.page["HoD Profiles"] = {}
        self.page["HoD Profiles"]["title"] = tk.Label(self, text = "Please select an action",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["HoD Profiles"]["button1"] = tk.Button(self, text = "Register New HoD", command=self.registerNewHoD,      bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["HoD Profiles"]["button2"] = tk.Button(self, text = "View HoD List", command=self.viewHoDList,            bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["HoD Profiles"]["button4"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admin"),         bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["HoD Profiles"].values():
            button.configure(width=20)

        self.page["Register New HoD"] = {}
        self.page["Register New HoD"]["title"] = tk.Label(self, text = "Please enter the hod's information below",              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["name label"] = tk.Label(self, text = "Name:",                                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["name entry"] = tk.Entry(self,                                                            bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["department label"] = tk.Label(self, text = "Department:",                                bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["department entry"] = tk.Entry(self,                                                      bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["email label"] = tk.Label(self, text = "E-mail address:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["email entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["phone label"] = tk.Label(self, text = "Phone No.",                                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["phone entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["address label"] = tk.Label(self, text = "Address:",                                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["address entry"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["honors gpa label"] = tk.Label(self, text = "Honors CGPA:",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["honors gpa entry"] = tk.Entry(self,                                                      bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["masters gpa label"] = tk.Label(self, text = "Masters CGPA:",                             bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New HoD"]["masters gpa entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New HoD"]["button"] = tk.Button(self, text = "Register", command=self.confirmHoDRegistration,       bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Register New HoD"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("HoD Profiles"),     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        
        self.page["Register New Teacher"] = {}
        self.page["Register New Teacher"]["title"] = tk.Label(self, text = "Please enter the teacher's information below",              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["name label"] = tk.Label(self, text = "Name:",                                                bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["name entry"] = tk.Entry(self,                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["department label"] = tk.Label(self, text = "Department:",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["department entry"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["email label"] = tk.Label(self, text = "E-mail address:",                                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["email entry"] = tk.Entry(self,                                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["phone label"] = tk.Label(self, text = "Phone No.",                                           bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["phone entry"] = tk.Entry(self,                                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["address label"] = tk.Label(self, text = "Address:",                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["address entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["honors gpa label"] = tk.Label(self, text = "Honors CGPA:",                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["honors gpa entry"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["masters gpa label"] = tk.Label(self, text = "Masters CGPA:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register New Teacher"]["masters gpa entry"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register New Teacher"]["button"] = tk.Button(self, text = "Register", command=self.confirmTeacherRegistration,       bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Register New Teacher"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("Teacher Profiles"),     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["Modify Teacher"] = {}
        self.page["Modify Teacher"]["username label"] = tk.Label(self, text = "Username:",                                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["username entry"] = tk.Label(self,                                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["name label"] = tk.Label(self, text = "Name:",                                              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["name entry"] = tk.Entry(self,                                                              bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["department label"] = tk.Label(self, text = "Department:",                                  bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["department entry"] = tk.Entry(self,                                                        bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["email label"] = tk.Label(self, text = "E-mail address:",                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["email entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["phone label"] = tk.Label(self, text = "Phone No.",                                         bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["phone entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["address label"] = tk.Label(self, text = "Address:",                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["address entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["honors gpa label"] = tk.Label(self, text = "Honors CGPA:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["honors gpa entry"] = tk.Entry(self,                                                        bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["masters gpa label"] = tk.Label(self, text = "Masters CGPA:",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Teacher"]["masters gpa entry"] = tk.Entry(self,                                                       bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Teacher"]["button"] = tk.Button(self, text = "Register", command=self.confirmTeacherModification,     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Modify Teacher"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("Teacher Profiles"),   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["admission"] = {}
        self.page["admission"]["title"] = tk.Label(self, text = "Please select an action",                                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["admission"]["button1"] = tk.Button(self, text = "Admit New Student", command=self.admitNewStudent,           bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admission"]["button2"] = tk.Button(self, text = "Register Old Student", command=self.registerOldStudent,     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admission"]["button3"] = tk.Button(self, text = "View Student List", command=self.viewStudentList,           bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["admission"]["button4"] = tk.Button(self, text = "Log Out", command=self.logout,                              bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        for button in self.page["admission"].values():
            button.configure(width=20)

        self.page["Admit New Student"] = {}
        self.page["Admit New Student"]["title"] = tk.Label(self, text = "Please enter the student's information below",     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["department label"] = tk.Label(self, text = "Department:",                           bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["department entry"] = tk.Entry(self,                                                 bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["semester label"] = tk.Label(self, text = "Semester:",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["semester entry"] = tk.Entry(self,                                                   bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["batch label"] = tk.Label(self, text = "Batch:",                                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["batch entry"] = tk.Entry(self,                                                      bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["name label"] = tk.Label(self, text = "Name:",                                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["name entry"] = tk.Entry(self,                                                       bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["dob label"] = tk.Label(self, text = "Date of Birth (dd/mm/yy):",                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["dob year"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["dob month"] = tk.Entry(self,                                                        bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["dob date"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["father's name label"] = tk.Label(self, text = "Father's Name:",                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["father's name entry"] = tk.Entry(self,                                              bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["mother's name label"] = tk.Label(self, text = "Mother's Name:",                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["mother's name entry"] = tk.Entry(self,                                              bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["email label"] = tk.Label(self, text = "E-mail address:",                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["email entry"] = tk.Entry(self,                                                      bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["phone label"] = tk.Label(self, text = "Phone No.",                                  bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["phone entry"] = tk.Entry(self,                                                      bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["address label"] = tk.Label(self, text = "Address:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["address entry"] = tk.Entry(self,                                                    bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["ssc gpa label"] = tk.Label(self, text = "SSC GPA:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["ssc gpa entry"] = tk.Entry(self,                                                    bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["hsc gpa label"] = tk.Label(self, text = "HSC GPA:",                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["hsc gpa entry"] = tk.Entry(self,                                                    bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["reference label"] = tk.Label(self, text = "Reference:",                             bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Admit New Student"]["reference entry"] = tk.Entry(self,                                                  bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Admit New Student"]["button"] = tk.Button(self, text = "Submit", command=self.submitInfoForAdmission,    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Admit New Student"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admission"),   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["Register Old Student"] = {}
        self.page["Register Old Student"]["title"] = tk.Label(self, text = "Please enter the student's information below",      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["department label"] = tk.Label(self, text = "Department:",                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["department entry"] = tk.Entry(self,                                                  bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["semester label"] = tk.Label(self, text = "Semester:",                                bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["semester entry"] = tk.Entry(self,                                                    bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["batch label"] = tk.Label(self, text = "Batch:",                                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["batch entry"] = tk.Entry(self,                                                       bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["name label"] = tk.Label(self, text = "Name:",                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["name entry"] = tk.Entry(self,                                                        bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["id label"] = tk.Label(self, text = "Student ID:",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["id entry"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["dob label"] = tk.Label(self, text = "Date of Birth (dd/mm/yy):",                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["dob year"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["dob month"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["dob date"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["father's name label"] = tk.Label(self, text = "Father's Name:",                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["father's name entry"] = tk.Entry(self,                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["mother's name label"] = tk.Label(self, text = "Mother's Name:",                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["mother's name entry"] = tk.Entry(self,                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["email label"] = tk.Label(self, text = "E-mail address:",                             bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["email entry"] = tk.Entry(self,                                                       bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["phone label"] = tk.Label(self, text = "Phone No.",                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["phone entry"] = tk.Entry(self,                                                       bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["address label"] = tk.Label(self, text = "Address:",                                  bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["address entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["ssc gpa label"] = tk.Label(self, text = "SSC GPA:",                                  bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["ssc gpa entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["hsc gpa label"] = tk.Label(self, text = "HSC GPA",                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["hsc gpa entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["reference label"] = tk.Label(self, text = "Reference:",                              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Register Old Student"]["reference entry"] = tk.Entry(self,                                                   bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Register Old Student"]["button"] = tk.Button(self, text = "Submit", command=self.submitInfoForRegistration,  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Register Old Student"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admission"),    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["Modify Student"] = {}
        self.page["Modify Student"]["title"] = tk.Label(self, text = "Please update the student's information below",           bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["id label"] = tk.Label(self, text = "Student ID:",                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["id entry"] = tk.Label(self, text = "",                                                     bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["department label"] = tk.Label(self, text = "Department:",                                  bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["department entry"] = tk.Entry(self,                                                        bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["semester label"] = tk.Label(self, text = "Semester:",                                      bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["semester entry"] = tk.Entry(self,                                                          bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["batch label"] = tk.Label(self, text = "Batch:",                                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["batch entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["name label"] = tk.Label(self, text = "Name:",                                              bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["name entry"] = tk.Entry(self,                                                              bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["dob label"] = tk.Label(self, text = "Date of Birth (dd/mm/yy):",                           bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["dob year"] = tk.Entry(self,                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["dob month"] = tk.Entry(self,                                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["dob date"] = tk.Entry(self,                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["father's name label"] = tk.Label(self, text = "Father's Name:",                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["father's name entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["mother's name label"] = tk.Label(self, text = "Mother's Name:",                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["mother's name entry"] = tk.Entry(self,                                                     bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["email label"] = tk.Label(self, text = "E-mail address:",                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["email entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["phone label"] = tk.Label(self, text = "Phone No.",                                         bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["phone entry"] = tk.Entry(self,                                                             bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["address label"] = tk.Label(self, text = "Address:",                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["address entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["ssc gpa label"] = tk.Label(self, text = "SSC GPA:",                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["ssc gpa entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["hsc gpa label"] = tk.Label(self, text = "HSC GPA",                                         bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["hsc gpa entry"] = tk.Entry(self,                                                           bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["reference label"] = tk.Label(self, text = "Reference:",                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Modify Student"]["reference entry"] = tk.Entry(self,                                                         bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Modify Student"]["button"] = tk.Button(self, text = "Modify", command=self.submitInfoForModification,        bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Modify Student"]["back"] = tk.Button(self, text = "Back", command=lambda:self.packAll("admission"),          bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["Change Password"] = {}
        self.page["Change Password"]["old password label"] = tk.Label(self, text = "Enter Old Password:",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Change Password"]["old password entry"] = tk.Entry(self, show="*",                                                   bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Change Password"]["new password label"] = tk.Label(self, text = "Enter New Password:",                               bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Change Password"]["new password entry"] = tk.Entry(self, show="*",                                                   bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Change Password"]["confirm password label"] = tk.Label(self, text = "Confirm New Password:",                         bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Change Password"]["confirm password entry"] = tk.Entry(self, show="*",                                               bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Change Password"]["button1"] = tk.Button(self, text = "Change Password", command=self.confirmPasswordChange,         bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Change Password"]["button2"] = tk.Button(self, text = "Back", command=lambda:self.packAll(self.loggedAccountType),   bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])

        self.page["View Teacher Info"] = {}
        
        self.page["View HoD Info"] = {}
        
        self.page["View Student Admission Info"] = {}

        self.page["Student List"] = {}
        
        self.page["Teacher List"] = {}
        
        self.page["hod List"] = {}

        self.packAll()

    def packAll(self, page="login"):
        self.i = 10
        self.j = 10
        self.labeltype = ""
        for widget in self.page[self.active_page].values():
            try:
                widget.delete(0, tk.END)
            except:
                pass
            widget.place_forget()
        self.active_page = page
        for widget in self.page[self.active_page].values():
            widget.place(x=self.j,y=self.i)
            if self.i > 500:
                self.i = 35
                self.j += 300
            else:
                self.i+=25

    def refreshStudentsList(self):
        for student in list(studentlist.values()):
            student.dump()

        for idno in [f for f in listdir(studentFolder) if isfile(join(studentFolder, f))]:
            with open(studentFolder + idno, 'rb') as infile:
                studentlist[idno[:-4]] = pickle.load(infile)

    def refreshTeachersList(self):
        for teacher in list(teacherlist.values()):
            teacher.dump()

        for username in [f for f in listdir(teacherFolder) if isfile(join(teacherFolder, f))]:
            with open(teacherFolder + username, 'rb') as infile:
                teacherlist[username[:-4]] = pickle.load(infile)

    def refreshHoDList(self):
        for hod in list(hodlist.values()):
            hod.dump()

        for username in [f for f in listdir(hodFolder) if isfile(join(hodFolder, f))]:
            with open(hodFolder + username, 'rb') as infile:
                hodlist[username[:-4]] = pickle.load(infile)
    
    def refreshCCSPList(self):
        for ccsp in list(ccsplist.values()):
            ccsp.dump()
                
        for ccsp in [f for f in listdir(ccspfolder) if isfile(join(ccspfolder, f))]:
            with open(ccspfolder + ccsp, 'rb') as infile:
                ccsplist[ccsp[:-4]] = pickle.load(infile)
        
    def login(self):
        if self.option.get() == "student":
            if self.page["login"]["username"].get() in list(studentlist.keys()):
                self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                if studentlist[self.page["login"]["username"].get()].checkPassword(self.page["login"]["password"].get()):
                    self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
                    self.loggedUsername = self.page["login"]["username"].get()
                    self.loggedDeparment = studentlist[self.page["login"]["username"].get()].returnDepartment()
                    self.packAll("student")
                else:
                    self.page["login"]["password label"].configure(text="Incorrect Password", fg="red")
            else:
                self.page["login"]["username label"].configure(text="Incorrect Username", fg="red")
                self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
        elif self.option.get() == "teacher":
            if self.page["login"]["username"].get() in list(teacherlist.keys()):
                self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                if teacherlist[self.page["login"]["username"].get()].checkPassword(self.page["login"]["password"].get()):
                    self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
                    self.loggedUsername = self.page["login"]["username"].get()
                    self.loggedDeparment = teacherlist[self.page["login"]["username"].get()].returnDepartment()
                    self.packAll("teacher")
                else:
                    self.page["login"]["password label"].configure(text="Incorrect Password", fg="red")
            else:
                self.page["login"]["username label"].configure(text="Incorrect Username", fg="red")
                self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
        elif self.option.get() == "hod":
            if self.page["login"]["username"].get() in list(hodlist.keys()):
                self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                if hodlist[self.page["login"]["username"].get()].checkPassword(self.page["login"]["password"].get()):
                    self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                    self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
                    self.loggedUsername = self.page["login"]["username"].get()
                    self.loggedDeparment = hodlist[self.page["login"]["username"].get()].returnDepartment()
                    self.packAll("hod")
                else:
                    self.page["login"]["password label"].configure(text="Incorrect Password", fg="red")
            else:
                self.page["login"]["username label"].configure(text="Incorrect Username", fg="red")
                self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
        elif self.option.get() == "administrative":
            if self.page["login"]["username"].get() == "admin":
                self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                if self.page["login"]["password"].get() == admin.returnPassword():
                    self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
                    self.packAll("admin")
                else:
                    self.page["login"]["password label"].configure(text="Incorrect Password", fg="red")
            elif self.page["login"]["username"].get() == "admission":
                self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])
                if self.page["login"]["password"].get() == specialAccessUserList["admission"].returnPassword():
                    self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])
                    self.packAll("admission")
                else:
                    self.page["login"]["password label"].configure(text="Incorrect Password", fg="red")
            elif self.page["login"]["username"].get() == "accounts":
                pass
            else:
                self.page["login"]["username label"].configure(text="Incorrect Username", fg="red")

    def resetUsername(self):
        self.page["login"]["username label"].configure(text="Username", fg=color["foreground"]["label"])

    def resetPassword(self):
        self.page["login"]["password label"].configure(text="Password", fg=color["foreground"]["label"])

    def logout(self):
        self.loggedUsername = ""
        self.packAll("login")
        
    def changePassword(self, userlist):
        self.packAll("Change Password")
        self.loggedAccountType = userlist
        
    def confirmPasswordChange(self):
        if self.loggedAccountType == "student":
            tempAccount = studentlist[self.loggedUsername]
        elif self.loggedAccountType == "teacher":
            tempAccount = teacherlist[self.loggedUsername]
        elif self.loggedAccountType == "hod":
            tempAccount = hodlist[self.loggedUsername]

        self.page["Change Password"]["old password entry"]
        self.page["Change Password"]["new password entry"]
        self.page["Change Password"]["confirm password entry"]
        if tempAccount.checkPassword(self.page["Change Password"]["old password entry"].get()):
            self.page["Change Password"]["old password label"].configure(text="Enter Old Password:", fg=color["foreground"]["label"])
            if self.page["Change Password"]["new password entry"].get() == self.page["Change Password"]["confirm password entry"].get():
                self.page["Change Password"]["confirm password label"].configure(text="Confirm New Password:", fg=color["foreground"]["label"])
                if self.loggedAccountType == "student":
                    studentlist[self.loggedUsername].changePassword(self.page["Change Password"]["new password entry"].get())
                elif self.loggedAccountType == "teacher":
                    teacherlist[self.loggedUsername].changePassword(self.page["Change Password"]["new password entry"].get())
                elif self.loggedAccountType == "hod":
                    hodlist[self.loggedUsername].changePassword(self.page["Change Password"]["new password entry"].get())
                self.packAll(self.loggedAccountType)
            else:
                self.page["Change Password"]["confirm password label"].configure(text="Passwords Don't Match", fg="red")
        else:
            self.page["Change Password"]["old password label"].configure(text="Password Incorrect", fg="red")

    def studentviewCCSP(self):
        pass

    def selectCourse(self):
        pass

    def viewRoutine(self):
        pass

    def viewCourses(self):
        pass

    def ccspManagement(self):
        self.page["CCSP Management"]["ccsp"].configure(text=ccsplist[hodlist[self.loggedUsername].returnDepartment()].view())
        self.packAll("CCSP Management")

    def addCourseToCCSP(self):
        ccsplist[hodlist[self.loggedUsername].returnDepartment()].addCourse(int(self.page["CCSP Management"]["semester"].get()), 
                                                         self.page["CCSP Management"]["course code"].get(), 
                                                         Course(self.page["CCSP Management"]["course code"].get(), 
                                                                self.page["CCSP Management"]["course name"].get(), 
                                                                self.page["CCSP Management"]["course credit"].get(), 
                                                                self.page["CCSP Management"]["prerequisite code"].get()
                                                                )
                                                         )
        self.page["CCSP Management"]["semester"].delete(0,tk.END)
        self.page["CCSP Management"]["course code"].delete(0,tk.END)
        self.page["CCSP Management"]["course name"].delete(0,tk.END)
        self.page["CCSP Management"]["course credit"].delete(0,tk.END)
        self.page["CCSP Management"]["prerequisite code"].delete(0,tk.END)
        self.ccspManagement()
    
    def removeCourseFromCCSP(self):
        self.ccspManagement()
    
    def hodviewCCSP(self):
        ccsplist[hodlist[self.loggedUsername].returnDepartment()].view("full")



    def studentManagement(self):
        pass

    def teacherManagement(self):
        pass

    def routineManagement(self):
        pass

    def openSpecialAccessUserPanel(self):
        self.packAll("Special Access Users")

    def changeAdmissionPassword(self):
        specialAccessUserList["admission"].changePassword(self.page["Special Access Users"]["admission password new"].get())
        self.page["Special Access Users"]["admission password"].configure(text = specialAccessUserList["admission"].returnPassword())

    def changeAccountsPassword(self):
        specialAccessUserList["accounts"].changePassword(self.page["Special Access Users"]["accounts password new"].get())
        self.page["Special Access Users"]["accounts password"].configure(text = specialAccessUserList["accounts"].returnPassword())

    def openAdminsAcademics(self):
        pass

    def openAdminsAccountSystem(self):
        pass

    def openAdminsTeacherProfile(self):
        self.packAll("Teacher Profiles")

    def openAdminsHoDProfile(self):
        self.packAll("HoD Profiles")
    
    def registerNewTeacher(self):
        self.packAll("Register New Teacher")
    
    def registerNewHoD(self):
        self.packAll("Register New HoD")
    
    def confirmHoDRegistration(self):
        self.department = self.page["Register New HoD"]["department entry"].get()
        self.username = self.page["Register New HoD"]["name entry"].get().replace(" ", "")
        self.newhod = HeadOfDepartment(self.username, self.department)
        
        self.newhod.setName(self.page["Register New HoD"]["name entry"].get())
        self.newhod.setEmail(self.page["Register New HoD"]["email entry"].get())
        self.newhod.setPhoneNo(self.page["Register New HoD"]["phone entry"].get())
        self.newhod.setAddress(self.page["Register New HoD"]["address entry"].get())
        self.newhod.setHonors(self.page["Register New HoD"]["honors gpa entry"].get())
        self.newhod.setMasters(self.page["Register New HoD"]["masters gpa entry"].get())
        
        hodlist[self.newhod.returnUsername()] = self.newhod
        self.refreshHoDList()

        self.viewHoD(hodlist[self.newhod.returnUsername()])
        if self.viewHoDNeedsBackButton:
            self.page["View HoD Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("HoD Profiles"),             bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.viewHoDNeedsBackButton = False
        self.packAll("View HoD Info")
        
    def confirmTeacherRegistration(self):
        self.department = self.page["Register New Teacher"]["department entry"].get()
        self.username = self.page["Register New Teacher"]["name entry"].get().replace(" ", "")
        self.newteacher = Teacher(self.username, self.department)
        
        self.newteacher.setName(self.page["Register New Teacher"]["name entry"].get())
        self.newteacher.setEmail(self.page["Register New Teacher"]["email entry"].get())
        self.newteacher.setPhoneNo(self.page["Register New Teacher"]["phone entry"].get())
        self.newteacher.setAddress(self.page["Register New Teacher"]["address entry"].get())
        self.newteacher.setHonors(self.page["Register New Teacher"]["honors gpa entry"].get())
        self.newteacher.setMasters(self.page["Register New Teacher"]["masters gpa entry"].get())
        
        teacherlist[self.newteacher.returnUsername()] = self.newteacher
        self.refreshTeachersList()

        self.viewTeacher(teacherlist[self.newteacher.returnUsername()])
        if self.viewTeacherNeedsBackButton:
            self.page["View Teacher Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("Teacher Profiles"),     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.viewTeacherNeedsBackButton = False
        self.packAll("View Teacher Info")
                                                                
    def confirmTeacherModification(self):
        teacherlist[self.teacherToBeModified].setName(self.page["Modify Teacher"]["name entry"].get())
        teacherlist[self.teacherToBeModified].setDepartment(self.page["Modify Teacher"]["department entry"].get())
        teacherlist[self.teacherToBeModified].setEmail(self.page["Modify Teacher"]["email entry"].get())
        teacherlist[self.teacherToBeModified].setPhoneNo(self.page["Modify Teacher"]["phone entry"].get())
        teacherlist[self.teacherToBeModified].setAddress(self.page["Modify Teacher"]["address entry"].get())
        teacherlist[self.teacherToBeModified].setHonors(self.page["Modify Teacher"]["honors gpa entry"].get())
        teacherlist[self.teacherToBeModified].setMasters(self.page["Modify Teacher"]["masters gpa entry"].get())
        
        self.refreshTeachersList()

        self.viewTeacher(teacherlist[self.teacherToBeModified])
        if self.viewTeacherNeedsBackButton:
            self.page["View Teacher Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("Teacher Profiles"),     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.viewTeacherNeedsBackButton = False
        self.packAll("View Teacher Info")

    def admitNewStudent(self):
        self.packAll("Admit New Student")

    def registerOldStudent(self):
        self.packAll("Register Old Student")

    def modifyStudent(self, studentID):
        self.modifyingID = studentID
        self.page["Modify Student"]["id entry"].configure(text=self.modifyingID)
        self.page["Modify Student"]["semester entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[3])
        self.page["Modify Student"]["department entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[5])
        self.page["Modify Student"]["batch entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[7])
        self.page["Modify Student"]["name entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[9])
        self.page["Modify Student"]["dob year"].insert(0, studentlist[self.modifyingID].returnInfoLong()[11][-2:])
        self.page["Modify Student"]["dob month"].insert(0, studentlist[self.modifyingID].returnInfoLong()[11][:2])
        self.page["Modify Student"]["dob date"].insert(0, studentlist[self.modifyingID].returnInfoLong()[11][3:-3])
        self.page["Modify Student"]["father's name entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[13])
        self.page["Modify Student"]["mother's name entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[15])
        self.page["Modify Student"]["email entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[17])
        self.page["Modify Student"]["phone entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[19])
        self.page["Modify Student"]["address entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[21])
        self.page["Modify Student"]["ssc gpa entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[23])
        self.page["Modify Student"]["hsc gpa entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[25])
        self.page["Modify Student"]["reference entry"].insert(0, studentlist[self.modifyingID].returnInfoLong()[27])
        self.packAll("Modify Student")

    def modifyTeacher(self, username):
        self.teacherToBeModified = username
        self.page["Modify Teacher"]["username entry"].configure(self.teacherToBeModified)
        self.page["Modify Teacher"]["name entry"].insert(0,teacherlist[self.teacherToBeModified].returnName())
        self.page["Modify Teacher"]["department entry"].insert(0,teacherlist[self.teacherToBeModified].returnDepartment())
        self.page["Modify Teacher"]["email entry"].insert(0,teacherlist[self.teacherToBeModified].returnEmail())
        self.page["Modify Teacher"]["phone entry"].insert(0,teacherlist[self.teacherToBeModified].returnPhoneNo())
        self.page["Modify Teacher"]["address entry"].insert(0,teacherlist[self.teacherToBeModified].returnAddress())
        self.page["Modify Teacher"]["honors gpa entry"].insert(0,teacherlist[self.teacherToBeModified].returnHonors())
        self.page["Modify Teacher"]["masters gpa entry"].insert(0,teacherlist[self.teacherToBeModified].returnMasters())
        self.packAll("Modify Teacher")

    def  submitInfoForAdmission(self):
        self.department = self.page["Admit New Student"]["department entry"].get()
        self.semester = int(self.page["Admit New Student"]["semester entry"].get())
        self.newstudent = Student(generateID(self.department, self.semester))
        self.newstudent.setBatch(int(self.page["Admit New Student"]["batch entry"].get()))
        self.newstudent.setDepartment(self.page["Admit New Student"]["department entry"].get())
        self.newstudent.setName(self.page["Admit New Student"]["name entry"].get())
        self.newstudent.setDoB(self.page["Admit New Student"]["dob year"].get(), self.page["Admit New Student"]["dob month"].get(), self.page["Admit New Student"]["dob date"].get())
        self.newstudent.setFathersName(self.page["Admit New Student"]["father's name entry"].get())
        self.newstudent.setMothersName(self.page["Admit New Student"]["mother's name entry"].get())
        self.newstudent.setEmail(self.page["Admit New Student"]["email entry"].get())
        self.newstudent.setPhoneNo(self.page["Admit New Student"]["phone entry"].get())
        self.newstudent.setAddress(self.page["Admit New Student"]["address entry"].get())
        self.newstudent.setSSC(self.page["Admit New Student"]["ssc gpa entry"].get())
        self.newstudent.setHSC(self.page["Admit New Student"]["hsc gpa entry"].get())
        self.newstudent.setReference(self.page["Admit New Student"]["reference entry"].get())

        studentlist[self.newstudent.returnID()] = self.newstudent
        self.refreshStudentsList()

        self.viewNewStudent(studentlist[self.newstudent.returnID()])
        if self.admissionNeedsBackButton:
            self.page["View Student Admission Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("admission"),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.admissionNeedsBackButton = False
        self.packAll("View Student Admission Info")
                                                                

    def submitInfoForRegistration(self):
        self.idno = self.page["Register Old Student"]["id entry"].get()
        self.oldstudent = Student(self.idno)
        self.oldstudent.setBatch(int(self.page["Register Old Student"]["batch entry"].get()))
        self.oldstudent.setSemester(int(self.page["Register Old Student"]["semester entry"].get()))
        self.oldstudent.setDepartment(self.page["Register Old Student"]["department entry"].get())
        self.oldstudent.setName(self.page["Register Old Student"]["name entry"].get())
        self.oldstudent.setDoB(self.page["Register Old Student"]["dob year"].get(), self.page["Register Old Student"]["dob month"].get(), self.page["Register Old Student"]["dob date"].get())
        self.oldstudent.setFathersName(self.page["Register Old Student"]["father's name entry"].get())
        self.oldstudent.setMothersName(self.page["Register Old Student"]["mother's name entry"].get())
        self.oldstudent.setEmail(self.page["Register Old Student"]["email entry"].get())
        self.oldstudent.setPhoneNo(self.page["Register Old Student"]["phone entry"].get())
        self.oldstudent.setAddress(self.page["Register Old Student"]["address entry"].get())
        self.oldstudent.setSSC(self.page["Register Old Student"]["ssc gpa entry"].get())
        self.oldstudent.setHSC(self.page["Register Old Student"]["hsc gpa entry"].get())
        self.oldstudent.setReference(self.page["Register Old Student"]["reference entry"].get())

        studentlist[self.oldstudent.returnID()] = self.oldstudent
        self.refreshStudentsList()

        self.viewNewStudent(studentlist[self.oldstudent.returnID()])
        if self.admissionNeedsBackButton:
            self.page["View Student Admission Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("admission"),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.admissionNeedsBackButton = False
        self.packAll("View Student Admission Info")
                                                                

    def submitInfoForModification(self):
        studentlist[self.modifyingID].setBatch(int(self.page["Modify Student"]["batch entry"].get()))
        studentlist[self.modifyingID].setSemester(int(self.page["Modify Student"]["semester entry"].get()))
        studentlist[self.modifyingID].setDepartment(self.page["Modify Student"]["department entry"].get())
        studentlist[self.modifyingID].setName(self.page["Modify Student"]["name entry"].get())
        studentlist[self.modifyingID].setDoB(self.page["Modify Student"]["dob year"].get(), self.page["Modify Student"]["dob month"].get(), self.page["Modify Student"]["dob date"].get())
        studentlist[self.modifyingID].setFathersName(self.page["Modify Student"]["father's name entry"].get())
        studentlist[self.modifyingID].setMothersName(self.page["Modify Student"]["mother's name entry"].get())
        studentlist[self.modifyingID].setEmail(self.page["Modify Student"]["email entry"].get())
        studentlist[self.modifyingID].setPhoneNo(self.page["Modify Student"]["phone entry"].get())
        studentlist[self.modifyingID].setAddress(self.page["Modify Student"]["address entry"].get())
        studentlist[self.modifyingID].setSSC(self.page["Modify Student"]["ssc gpa entry"].get())
        studentlist[self.modifyingID].setHSC(self.page["Modify Student"]["hsc gpa entry"].get())
        studentlist[self.modifyingID].setReference(self.page["Modify Student"]["reference entry"].get())

        self.refreshStudentsList()

        self.viewNewStudent(studentlist[self.modifyingID])
        if self.admissionNeedsBackButton:
            self.page["View Student Admission Info"]["x"] = tk.Button(self, text="Back", command=lambda:self.packAll("admission"),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
            self.admissionNeedsBackButton = False
        self.packAll("View Student Admission Info")

    def viewTeacherList(self):
        self.page["Teacher List"]["x1"] = tk.Label(self, text="Enter a Username",                                                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Teacher List"]["x2"] = tk.Entry(self,                                                                                            bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Teacher List"]["x3"] = tk.Button(self, text="Modify", command=lambda:self.modifyTeacher(self.page["Teacher List"]["x2"].get()),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher List"]["x4"] = tk.Button(self, text="Make HoD", command=lambda:self.makeHoD(self.page["Teacher List"]["x2"].get()),      bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher List"]["x5"] = tk.Button(self, text="Back", command=lambda:self.packAll("Teacher Profiles"),                             bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Teacher List"]["titles"] = tk.Label(self, text = "Department\tName",                                                             bg=color["background"]["label"], fg=color["foreground"]["label"])
        for teacher in list(teacherlist.values()):
            self.page["Teacher List"][teacher.returnUsername()] = tk.Label(self, text="\t\t".join(teacher.returnInfoShort()),                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("Teacher List")

    def viewHoDList(self):
        self.page["hod List"]["x1"] = tk.Label(self, text="Enter a Username",                                                                       bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["hod List"]["x2"] = tk.Entry(self,                                                                                                bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["hod List"]["x3"] = tk.Button(self, text="Modify", command=lambda:self.modifyhod(self.page["hod List"]["x2"].get()),              bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod List"]["x4"] = tk.Button(self, text="Make HoD", command=lambda:self.makeHoD(self.page["hod List"]["x2"].get()),              bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod List"]["x5"] = tk.Button(self, text="Back", command=lambda:self.packAll("HoD Profiles"),                                     bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["hod List"]["titles"] = tk.Label(self, text = "Department\tName",                                                                 bg=color["background"]["label"], fg=color["foreground"]["label"])
        for hod in list(hodlist.values()):
            self.page["hod List"][hod.returnUsername()] = tk.Label(self, text="\t\t".join(hod.returnInfoShort()),                                   bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("hod List")

    def viewStudentList(self):
        self.page["Student List"]["x1"] = tk.Label(self, text="Enter an ID",                                                                        bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.page["Student List"]["x2"] = tk.Entry(self,                                                                                            bg=color["background"]["entry"], fg=color["foreground"]["entry"])
        self.page["Student List"]["x3"] = tk.Button(self, text="Modify", command=lambda:self.modifyStudent(self.page["Student List"]["x2"].get()),  bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student List"]["x4"] = tk.Button(self, text="Back", command=lambda:self.packAll("admission"),                                    bg=color["background"]["button"], fg=color["foreground"]["button"], activebackground=color["activebackground"]["button"], activeforeground=color["activeforeground"]["button"])
        self.page["Student List"]["titles"] = tk.Label(self, text = "Student ID\t\tName\t\t\tDepartment\tBatch\tSemester",                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        for student in list(studentlist.values()):
            self.page["Student List"][student.returnID()] = tk.Label(self, text="\t\t".join(student.returnInfoShort()),                             bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("Student List")

    def viewStudent(self):
        pass

    def viewNewStudent(self, student = Student()):
        for i in range(len(student.returnInfoLong())):
            self.page["View Student Admission Info"][i] = tk.Label(self, text=student.returnInfoLong()[i],                                          bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("View Student Admission Info")

    def viewTeacher(self, teacher = Teacher()):
        for i in range(len(teacher.returnInfoLong())):
            self.page["View Teacher Info"][i] = tk.Label(self, text=teacher.returnInfoLong()[i],                                                    bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("View Teacher Info")

    def viewHoD(self, hod = HeadOfDepartment()):
        for i in range(len(hod.returnInfoLong())):
            self.page["View HoD Info"][i] = tk.Label(self, text=hod.returnInfoLong()[i],                                                            bg=color["background"]["label"], fg=color["foreground"]["label"])
        self.packAll("View HoD Info")


        
        



#design old student registration and double-checking system



# page["login"]["title"].place(x=50, y=50)
# page["login"]["instructions"].place(x=55, y=90)

# for i in range(4):
#     page["login"]["option"+str(i+1)].place(x=55, y=110+20*i)

# page["login"]["username"].place(x=225, y=130)
# page["login"]["password"].place(x=225, y=150)
# page["login"]["loginbutton"].place(x=225, y=170)
