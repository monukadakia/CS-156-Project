import sys
import math

import requirements


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
        self.math_req = None
        self.taking = []
        self.final_schedule = []
        self.kb = KB()
        self.total_cls = None
        self.user_pref = None
     

    def start_scheduling(self):
        self.math_req = raw_input("Have you met the math requirement?(Y/N) ").replace(" ", "").upper()
        while not(self.math_req == 'Y' or self.math_req == 'N'):
            self.math_req = raw_input("Have you met the math requirement?(Y/N) ").replace(" ", "").upper()

        self.user_pref = raw_input("How many classes do you want to take?(4 or 5) ").replace(" ", "").upper()
        while not(self.user_pref == '4' or self.user_pref == '5'):
            self.user_pref = raw_input("How many classes do you want to take?(4/5) ").replace(" ", "").upper()
        if self.math_req == 'Y':
            self.kb.tell("MATH19")
            self.final_schedule.append("MATH30") 
            self.final_schedule.append("CS46A") 
        elif self.math_req == 'N':
            self.final_schedule.append("MATH19")
        self.user_pref = int(self.user_pref)
        self.add_GEs(self.final_schedule, self.user_pref)
        self.print_final_schedule(self.final_schedule)
        self.askGrades(self.final_schedule)
        self.calculateDiff(self.getFileData())

    def print_final_schedule(self, final_schedule):
        counter = 1
        for x in final_schedule:
            print "%d. %s" %(counter, x)
            counter += 1

    def add_GEs(self, final_schedule, user_pref):
        counter = 1
        for x in range(user_pref-len(final_schedule)):
            final_schedule.append("GE Class %d" %(counter))
            counter += 1
        return final_schedule

    def askGrades(self, final_schedule):
        CSGPA = 0
        CSCT = 0
        GECT = 0
        GEGPA = 0
        file_data = self.getFileData()
        grade = None
        requirement = requirements.Classes()
        for x in final_schedule:
            grade = raw_input(("What was your grade in %s: " %(x))).replace(" ", "").upper()
            if not("GE Class" in x):
                CSGPA += requirement.grade[grade]
                CSCT += 1
                if(x in file_data):
                    file_data[x] += ("%s," % (grade))
                else:
                    file_data[x] = ("%s," % (grade))
            else:
                GEGPA += requirement.grade[grade]
                GECT += 1
        print "CS GPA: ", CSGPA/CSCT
        print "GE GPA: ", GEGPA/GECT
        self.addGradeToFile(file_data)
      
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
            difficulty[cls] = total
        print difficulty
        return difficulty










            
           

      


        

           



user = Agent()
user.start_scheduling()
