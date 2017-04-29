import sys

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
        self.classAvailable = None
        self.kb = KB()

    def initial_question(self):
        self.user_input = raw_input("Please enter list of latest Math and CS classes separated by a comma. For eg, CS46A,CS49C : ").replace(" ", "").upper()
        self.listOfClasses = self.user_input.split(",")
        requirement = requirements.Classes()
        grades = 0
        
        for cls in self.listOfClasses:
            gradeInput = raw_input("Grade for %s :" % (cls)).upper().replace(" ", "")
            grades += requirement.grade[gradeInput]
        
        gpa = 0 ## Calculate the GPA

        if not("CS100W" in self.listOfClasses):
            self.wst = raw_input("Have you passed WST? Please enter 'Y' or 'N': ").upper()
            while not(self.wst == "Y" or self.wst == "N"):
                self.wst = raw_input("Please enter 'Y' or 'N'. Have you passed WST? : ").upper()
            if self.wst == 'Y':
                self.taken = True
        else:
            self.taken = True

        
        

        #for cls in self.listOfClasses:
        #    self.kb.tell(cls)
        #    for clause in self.kb.clauses:
        #        x = requirement.classes[clause].replace(" ", "").split(",")
        #        for xs in x:
        #            self.kb.tell(xs)
        self.addClasses(self.listOfClasses)
        print self.kb.clauses

        for a_class in requirement.classes:
            x = requirement.classes[a_class].replace(" ", "").split(",")
            b = True
            if a_class == "CS100W" and self.taken and not("CS100W" in self.kb.clauses):
                print "Next sem you can take:",a_class
            else:
                for classes in x:
                    if not(classes in self.kb.clauses):
                        b = False
                        break
                if b and not(a_class in self.kb.clauses):
                    print "Next sem you can take:",a_class

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



user = Agent()
user.initial_question()
