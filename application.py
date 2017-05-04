import sys
import math

import requirements

# tester = {"CS46A": "CS46B"};
#
# taken = False
#
# var = raw_input("Please enter List of Class separated by a comma. For eg, CS46A,CS49C : ")
# wst = raw_input("Have you passed WST? Please enter 'Y' or 'N': ").upper()
#
#
# while not(wst == "Y" or wst == "N"):
#     wst = raw_input("Please enter 'Y' or 'N'. Have you passed WST? : ").upper()
#
# if wst == 'Y' or wst == 'N':
#     if wst == 'Y':
#         taken = True
#
# var = var.replace(" ", "").upper();
# listOfClasses = var.split(",")
#
# for a_class in listOfClasses:
#     if(a_class == "CS46A"):
#         print "For next semester you can take ", tester['CS46A']
#
# print "you entered", listOfClasses
# print "User has passed WST", taken

class KB(object):
    """docstring for KB"""

    def __init__(self):
        super(KB, self).__init__()
        self.clauses = []

    def tell(self, clause):
        if not(clause in self.clauses) and not(clause == None):
            self.clauses.append(clause)

    def ask(self, clause):
        return clause in self.clauses


class Agent(object):
    """docstring for Agent."""


    def __init__(self):
        super(Agent, self).__init__()
        self.wst = None
        self.taken = False
        self.user_input = None
        self.listOfClasses = None
        self.classAvailable = []
        self.kb = KB()
        self.difficultyLevel = 0

    def initial_question(self):
        #calculateDiff()
        #self.getFileData()

        self.user_input = raw_input("Please enter list of latest Math and CS classes separated by a comma. For eg, CS46A,CS49C : ").replace(" ", "").upper()
        self.listOfClasses = self.user_input.split(",")
        requirement = requirements.Classes()

        self.addClasses(self.listOfClasses)
        file_data = self.getFileData()

        grades = {}

        for cls in self.kb.clauses:
            gradeInput = raw_input("Grade for %s :" % (cls)).upper().replace(" ", "")
            grades[cls] = gradeInput
            #grade = requirement.grade[gradeInput] * 3
            file_data[cls] += ("%s," % (gradeInput))

        self.addGradeToFile(file_data)
        difficulty = self.calculateDiff(file_data)
        print difficulty

        if not("CS100W" in self.listOfClasses):
            self.wst = raw_input("Have you passed WST? Please enter 'Y' or 'N': ").upper()
            while not(self.wst == "Y" or self.wst == "N"):
                self.wst = raw_input("Please enter 'Y' or 'N'. Have you passed WST? : ").upper()
            if self.wst == 'Y':
                self.taken = True
        else:
            self.taken = True

        if self.taken and not("CS100W" in self.kb.clauses):
                print "Next sem you can take: CS100W"
                self.classAvailable.append('CS100W')
        for a_class in requirement.classes:
            x = requirement.classes[a_class].replace(" ", "").split(",")
            b = True
            for classes in x:
                if not(classes in self.kb.clauses):
                    b = False
                    break
            if b and not(a_class in self.kb.clauses):
                print "Next sem you can take:",a_class
                self.classAvailable.append(a_class)

        recommend = {1:"",2:"",3:""}
        for cls in self.classAvailable:
            recommend[difficulty[cls]] += ("%s," % (cls))

        print recommend

        #self.finalClass(self.classAvailable, grades)

        print "you entered", self.listOfClasses
        print "User has passed WST", self.taken

    def addClasses(self, classes):
        requirement = requirements.Classes()
        if len(classes) == 1 and not (classes[0] in requirement.classes):
            self.kb.tell(classes[0])
            return classes[0]
        else:
            for cl in classes:
                self.kb.tell(cl)
                if cl in requirement.classes:
                    self.kb.tell(self.addClasses(requirement.classes[cl].replace(" ", "").split(",")))

    def addGradeToFile(self,file_data):
        file_object = open("grade.txt", "w")
        for cls in file_data:
            temp = cls
            temp += (":%s\n" % (file_data[cls]))
            file_object.write(temp)

    def getFileData(self):
        file_object = open("grade.txt", "r")
        hashmap = {}
        for x in file_object.readlines():
            x = x.strip()
            name = x[0:x.index(':')]
            data = ""
            if not(x[len(x)-1] == ':'):
                data = x[x.index(':')+1:len(x)]
            hashmap[name] = data
        return hashmap

    def calculateDiff(self, file_data):
        requirement = requirements.Classes()
        difficulty = {}
        for cls in file_data:
            temp = file_data[cls].split(",")
            temp.remove('')
            total = 0
            for grd in temp:
                if not(grd.strip() == ''):
                    total += requirement.grade[grd]
            if len(temp) > 0:
                total = total / (len(temp))
            if total >= 3.5:
                difficulty[cls] = 1
            elif total >= 3:
                difficulty[cls] = 2
            else:
                difficulty[cls] = 3
        return difficulty

    # def finalClasses(self, classAvailable, grades):
    #     requirement = requirements.Classes()
    #     if(len(classAvailable) <= 3)
    #         return classAvailable
    #     else   
    #         for next_class in classAvailable:
    #             clss = requirement[next_class].replace(" ", "").split(",")
    #             for cls in clss:
    #                 grade = grades[cls]

            



user = Agent()
user.initial_question()
