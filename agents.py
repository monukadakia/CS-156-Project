import sys
import math
import Graph
import requirements
import random


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
        self.quit = None
        self.CSGPA = None
        self.GEGPA = None
        self.ratio = (0,0)
        self.classAvailable = []
        self.performance = 0

    def start_scheduling(self):
        self.math_req = raw_input("Have you met the math requirement?(Y/N) ").replace(" ", "").upper()
        while not(self.math_req == 'Y' or self.math_req == 'N'):
            self.math_req = raw_input("Have you met the math requirement?(Y/N) ").replace(" ", "").upper()

        self.user_pref = raw_input("How many classes do you want to take?(4 or 5) ").replace(" ", "").upper()
        while not(self.user_pref == '4' or self.user_pref == '5'):
            self.user_pref = raw_input("How many classes do you want to take?(4/5) ").replace(" ", "").upper()
        self.user_pref = int(self.user_pref)


        if self.math_req == 'Y':
            self.kb.tell("MATH19")
            self.ratio = (2,self.user_pref-2)
            self.findClasses()
        else:
            self.final_schedule.append("MATH19")
            self.ratio = (1,self.user_pref-1)




        # if self.math_req == 'Y':
        #     self.kb.tell("MATH19")
        #     self.final_schedule.append("MATH30")
        #     self.final_schedule.append("CS46A")
        #     self.ratio = (2,self.user_pref-2)
        # elif self.math_req == 'N':
        #     self.final_schedule.append("MATH19")
        #     self.ratio = (1,self.user_pref-1)
        # self.add_GEs(self.final_schedule, self.user_pref)
        # self.print_final_schedule(self.final_schedule)
        # self.askGrades(self.final_schedule)
        # self.calculateDiff(self.getFileData())
        while(True):
            print "final_schedule: ", self.final_schedule
            if len(self.final_schedule) > 0:
                if (self.ratio[0] > len(self.final_schedule)):
                    gph = Graph.Graph()
                    gph.create_weighted_graph(self.calculateDiff(self.getFileData()))
                    if len(self.classAvailable) > self.ratio[0]-len(self.final_schedule):
                        x = gph.BFS(gph.g, "MATH19", self.classAvailable, self.ratio[0]-len(self.final_schedule))
                        for xs in x:
                            self.final_schedule.append(xs)
                    elif len(self.classAvailable) < self.ratio[0]-len(self.final_schedule):
                        temp = len(self.final_schedule) + len(self.classAvailable)
                        self.ratio = (temp, (self.ratio[0] + self.ratio[1]) - temp)
                        for x in self.classAvailable:
                            self.final_schedule.append(x)
                    else:
                        for x in self.classAvailable:
                            self.final_schedule.append(x)
                elif self.ratio[0] < len(self.final_schedule):
                    gph = Graph.Graph()
                    gph.create_weighted_graph(self.calculateDiff(self.getFileData()))
                    self.final_schedule = gph.BFS(gph.g, "MATH19", self.final_schedule, self.ratio[0])
            elif(self.ratio[0] < len(self.classAvailable)):
                gph = Graph.Graph()
                gph.create_weighted_graph(self.calculateDiff(self.getFileData()))
                self.final_schedule = gph.BFS(gph.g, "MATH19", self.classAvailable, self.ratio[0])
            elif self.ratio[0] == len(self.classAvailable):
                self.final_schedule = self.classAvailable
            print "Ratio ", self.ratio
            self.add_GEs(self.final_schedule, self.user_pref)
            self.print_final_schedule(self.final_schedule)
            self.askGrades(self.final_schedule)
            self.calculateDiff(self.getFileData())
            print "CSGPA", self.CSGPA
            print "GEGPA", self.GEGPA
            # print self.kb.clauses
            # print "CSGPA", self.CSGPA
            # print "GEGPA", self.GEGPA
            # print "BRatio", self.ratio
            # self.quit = raw_input("Press q to quit or enter to continue: ").replace(" ", "").upper().strip()
            # if(self.quit == 'Q'):
            #     break
            #else:
            #self.findClasses()
            if(self.CSGPA >= 3.3 and self.GEGPA >= 3.3 and self.ratio[0] + self.ratio[1] < 5):
                self.ratio = random.choice([(self.ratio[0]+1,self.ratio[1]), (self.ratio[0],self.ratio[1]+1)])
            elif(self.CSGPA >= 3.3 and self.ratio[0] < 4 and self.ratio[1] > 1 and self.GEGPA < 3.3):
                if(self.ratio[0] + self.ratio[1] < 5 and self.GEGPA >= 3.0):
                    self.ratio = (self.ratio[0]+1,self.ratio[1])
                else:
                    self.ratio = (self.ratio[0]+1,self.ratio[1]-1)
            elif(self.GEGPA >= 3.3 and self.ratio[1] < 4 and self.ratio[0] > 1 and self.CSGPA < 3.3):
                if(self.ratio[1] + self.ratio[0] < 5):
                    self.ratio = (self.ratio[0],self.ratio[1]+1)
                else:
                    self.ratio = (self.ratio[0]-1,self.ratio[1]+1)
            elif(self.CSGPA <= 2.0 and self.GEGPA <= 2.0):
                print "Your GPA is too low. Please take a semester off."
            elif(self.CSGPA < 3.3 and self.CSGPA < 3.3 and self.ratio[0] > 1 and self.ratio[1] > 1):
                self.ratio = (self.ratio[0]-1,self.ratio[1]-1)
            elif(self.CSGPA < 3.3 and self.ratio[0] > 1):
                self.ratio = (self.ratio[0]-1,self.ratio[1])
            elif(self.GEGPA < 3.3 and self.ratio[1] > 1):
                self.ratio = (self.ratio[0],self.ratio[1]-1)

            if ("MATH19" in self.final_schedule):
                self.final_schedule = []
                self.final_schedule.append("CS46A")
                self.final_schedule.append("MATH30")
            elif len(self.classAvailable) > 0:
                self.final_schedule = []
                if self.ratio[0] == len(self.classAvailable):
                    self.final_schedule = self.classAvailable
                elif self.ratio[0] > len(self.classAvailable):
                    self.final_schedule = self.classAvailable
                    self.classAvailable = []
                    self.findClasses()
                    print "After updating: ", self.classAvailable
                    for cls in self.classAvailable:
                        if cls in self.final_schedule:
                            self.classAvailable.remove(cls)
            else:
                self.final_schedule = []
                self.findClasses()
                if(self.ratio[0] == len(self.classAvailable)):
                    self.final_schedule = self.classAvailable
                elif(self.ratio[0] > len(self.classAvailable)):
                    self.ratio = (len(self.classAvailable),self.ratio[1]+1)
            self.quit = raw_input("Press q to quit or enter to continue: ").replace(" ", "").upper().strip()
            if(self.quit == 'Q'):
                break

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
        self.CSGPA = 0
        CSCT = 0
        GECT = 0
        self.GEGPA = 0
        file_data = self.getFileData()
        grade = None
        requirement = requirements.Classes()
        self.findClasses()
        for x in final_schedule:
            grade = raw_input(("What was your grade in %s: " %(x))).replace(" ", "").upper()
            while not(grade in requirement.grade):
                grade = raw_input(("What was your grade in %s: " %(x))).replace(" ", "").upper()
            self.evalPerformance(requirement.grade[grade])
            if not("GE Class" in x):
                if "MATH19" != x:
                    self.classAvailable.remove(x)
                self.CSGPA += requirement.grade[grade]
                CSCT += 1
                self.kb.tell(x)
                if(x in file_data):
                    file_data[x] += ("%s," % (grade))
                else:
                    file_data[x] = ("%s," % (grade))
            else:
                self.GEGPA += requirement.grade[grade]
                GECT += 1
        print "Agent's performance", self.performance
        if CSCT > 0:
            self.CSGPA = self.CSGPA/CSCT
        if GECT > 0:
            self.GEGPA = self.GEGPA/GECT
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
        return difficulty

    def findClasses(self):
        requirement = requirements.Classes()
        for cls in requirement.classes:
            x = requirement.classes[cls].replace(" ", "").split(",")
            b = True
            for classes in x:
                if not(self.kb.ask(classes)):
                    b = False
                    break
            if b and not(cls in self.kb.clauses):
                self.classAvailable.append(cls)

    def evalPerformance(self, grade):
        if(grade >= 3.7):
            self.performance += 10
        elif(grade >= 2.7):
            self.performance += 5
        elif(grade >= 1.7):
            self.performance -= 5
        else:
            self.performance -= 20
            

user = Agent()
user.start_scheduling()
