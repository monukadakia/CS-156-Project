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



class gradAgent(object):
    def __init__(self, user_pref, math_req):
        super(gradAgent, self).__init__()
        self.geCounter = 15
        self.csCounter = 24
        self.kinCounter = 2
        self.math_req = math_req
        self.taking = []
        self.final_schedule = []
        self.kb = KB()
        self.total_cls = None
        self.user_pref = user_pref
        self.quit = None
        #self.CSGPA = None
        #self.GEGPA = None
        self.ratio = (0,0)
        self.classAvailable = []
        self.performance = 0
        self.overallGPA = 0
        self.overallCnt = 0
        self.start_scheduling()

    def start_scheduling(self):
        if self.math_req == 'Y':
            self.kb.tell("MATH19")
            self.ratio = (2,self.user_pref-2)
            self.findClasses()
        else:
            self.final_schedule.append("MATH19")
            self.ratio = (1,self.user_pref-1)
            self.csCounter = 25

        while(True):

            if len(self.final_schedule) > 0:    #Checks to see if final_schedule has classes in it
                if (self.ratio[0] > len(self.final_schedule)):      #if  cs ratio is greater than list of final schedule
                    gph = Graph.Graph()     #create the graph
                    gph.create_weighted_graph(self.calculateDiff(self.getFileData()))       #get the weighted graph
                    if len(self.classAvailable) > self.ratio[0]-len(self.final_schedule):   #if length of classes available is greater than remaining classes
                        x = gph.BFS_graduation(gph.g, "MATH19", self.classAvailable, self.ratio[0]-len(self.final_schedule))       #get the list of best classes
                        for xs in x:    #for all classes in the best classes
                            if not xs in self.final_schedule:   #if final schedule does not have the class
                                self.final_schedule.append(xs)      #then append it
                    elif len(self.classAvailable) < self.ratio[0]-len(self.final_schedule): #if classes available are less than the remaining classes
                        temp = len(self.final_schedule) + len(self.classAvailable)      #temp is total number of classes
                        self.ratio = (temp, (self.ratio[0] + self.ratio[1]) - temp)     #update the ratio
                        for x in self.classAvailable:       #for all the classes in classes available
                            if not x in self.final_schedule:        #if the class is not in final_schedule
                                self.final_schedule.append(x)       #then append it
                    else:       # if length of classes available is equal to length of remaining class
                        for x in self.classAvailable:       #for all the classes in class available
                            if not x in self.final_schedule:    #if class is not in final_schedule
                                self.final_schedule.append(x)       # then append it
                elif self.ratio[0] < len(self.final_schedule):
                    gph = Graph.Graph()
                    gph.create_weighted_graph(self.calculateDiff(self.getFileData()))
                    self.final_schedule = gph.BFS_graduation(gph.g, "MATH19", self.final_schedule, self.ratio[0])
            elif(self.ratio[0] < len(self.classAvailable)):
                gph = Graph.Graph()
                gph.create_weighted_graph(self.calculateDiff(self.getFileData()))
                self.final_schedule = gph.BFS_graduation(gph.g, "MATH19", self.classAvailable, self.ratio[0])
            elif self.ratio[0] == len(self.classAvailable):
                for x in self.classAvailable:
                    self.final_schedule.append(x)
            if self.kinCounter > 0:
                self.final_schedule.append("KIN Class")
            self.add_GEs(self.final_schedule, self.ratio[0] + self.ratio[1])
            self.print_final_schedule(self.final_schedule)
            self.askGrades(self.final_schedule)
            self.calculateDiff(self.getFileData())

            if(self.ratio[0] + self.ratio[1] == 6):
                self.ratio = (self.ratio[0], self.ratio[1]-1)
            if(self.csCounter <= 0 and self.geCounter <= 0 and self.kinCounter <= 0):
                print "CONGRATULATIONS!!! You have graduated :)"
                break
            # print self.kb.clauses
            # print "CSGPA", self.CSGPA
            # print "GEGPA", self.GEGPA
            # print "BRatio", self.ratio
            # self.quit = raw_input("Press q to quit or enter to continue: ").replace(" ", "").upper().strip()
            # if(self.quit == 'Q'):
            #     break
            #else:
            #self.findClasses()

            if(self.CSGPA >= 3.3 and self.GEGPA >= 3.3):
                if(self.ratio[0] + self.ratio[1] < 5):
                    if(self.ratio[0] < 4):
                        self.ratio = (self.ratio[0] + 1, self.ratio[1])
                    else:
                        self.ratio = (self.ratio[0], self.ratio[1] + 1)
                else:
                    if(self.ratio[0] < 4):
                        self.ratio = (self.ratio[0] + 1, self.ratio[1] - 1)
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
            elif(self.CSGPA < 3.3 and self.GEGPA < 3.3 and self.ratio[0] > 1 and self.ratio[1] > 1):
                if not self.overallGPA > 3.0:
                    self.ratio = (self.ratio[0]-1,self.ratio[1]-1)
                    print "The agent can not meet 4 year goal because your GPA is considerably low"
            elif(self.CSGPA < 3.3 and self.ratio[0] > 1):
                self.ratio = (self.ratio[0] - 1,self.ratio[1])

            elif(self.GEGPA < 3.3 and self.ratio[1] > 1):
                self.ratio = (self.ratio[0],self.ratio[1]-1)

            if ("MATH19" in self.final_schedule):
                self.final_schedule = []
                self.final_schedule.append("CS46A")
                self.final_schedule.append("MATH30")
            elif len(self.classAvailable) > 0:
                self.final_schedule = []
                if self.ratio[0] == len(self.classAvailable):
                    for x in self.classAvailable:       #for all the classes in classes available
                        if not x in self.final_schedule:        #if the class is not in final_schedule
                            self.final_schedule.append(x)       #then append it
                elif self.ratio[0] > len(self.classAvailable):
                    for x in self.classAvailable:       #for all the classes in classes available
                        if not x in self.final_schedule:        #if the class is not in final_schedule
                            self.final_schedule.append(x)       #then append it
                    self.classAvailable = []
                    self.findClasses()
                    for cls in self.classAvailable:
                        if cls in self.final_schedule:
                            self.classAvailable.remove(cls)
            else:
                self.final_schedule = []
                self.findClasses()
                if(self.ratio[0] == len(self.classAvailable)):
                    for x in self.classAvailable:       #for all the classes in classes available
                        if not x in self.final_schedule:        #if the class is not in final_schedule
                            self.final_schedule.append(x)       #then append it
                elif(self.ratio[0] > len(self.classAvailable)):
                    totalClasses = self.ratio[0] + self.ratio[1]
                    self.ratio = (len(self.classAvailable), totalClasses - len(self.classAvailable))



            if self.csCounter < self.ratio[0] and self.geCounter < self.ratio[1]:
                self.ratio = (self.csCounter, self.geCounter)
            elif self.csCounter < self.ratio[0]:
                if (self.ratio[0] + self.ratio[1])-self.csCounter <= self.geCounter:
                    self.ratio = (self.csCounter, (self.ratio[0] + self.ratio[1])-self.csCounter)
                else:
                    self.ratio = (self.csCounter, self.geCounter)
            elif self.geCounter < self.ratio[1]:
                if (self.ratio[0] + self.ratio[1])-self.geCounter <= self.csCounter:
                    self.ratio = ((self.ratio[0] + self.ratio[1])-self.geCounter, self.geCounter)
                else:
                    self.ratio = (self.csCounter, self.geCounter)
            self.quit = raw_input("Press q to quit or enter to continue: ").replace(" ", "").upper().strip()
            if self.kinCounter > 0:
                self.user_pref += 1
                self.ratio = (self.ratio[0], self.ratio[1]+1)
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
            if not("Class" in x):
                if "MATH19" != x:
                    self.classAvailable.remove(x)
                self.CSGPA += requirement.grade[grade] * 3
                self.overallGPA += requirement.grade[grade] * 3
                CSCT += 3
                self.overallCnt += 3
                self.kb.tell(x)
                if(x in file_data):
                    file_data[x] += ("%s," % (grade))
                else:
                    file_data[x] = ("%s," % (grade))
                if requirement.grade[grade]>=1.7:
                    self.csCounter -= 1
                else:
                    if not x in self.final_schedule:
                        self.final_schedule.append(x)
            elif "GE Class" in x:
                self.GEGPA += requirement.grade[grade] * 3
                self.overallGPA += requirement.grade[grade] * 3
                GECT += 3
                self.overallCnt += 3
                if(requirement.grade[grade] >= 1.7):
                    self.geCounter -= 1
            else:
                self.GEGPA += requirement.grade[grade]
                self.overallGPA += requirement.grade[grade]
                GECT += 1
                self.overallCnt += 1
                if(requirement.grade[grade] >= 1.7):
                    self.kinCounter -= 1
        print "Agent's performance", self.performance
        if CSCT > 0 and self.csCounter > 0:
            self.CSGPA = self.CSGPA/CSCT
        if GECT > 0 and self.geCounter > 0:
            self.GEGPA = self.GEGPA/GECT
        print "Overall GPA:", round(self.overallGPA/self.overallCnt, 3)
        if round(self.overallGPA/self.overallCnt, 3) <= 2.9:
            print "NOTICE: The agent can no longer satisfy 4 year graduation plan"
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
            if b and not(cls in self.kb.clauses) and not(cls in self.classAvailable):
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

#
# user = Agent()
#user.start_scheduling()
