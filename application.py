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


class Agent(object):
    """docstring for Agent."""


    def __init__(self):
        super(Agent, self).__init__()
        self.wst = None
        self.taken = False
        self.user_input = None
        self.listOfClasses = None
        self.classAvailable = None

    def initial_question(self):
        self.user_input = raw_input("Please enter List of Class separated by a comma. For eg, CS46A,CS49C : ").replace(" ", "").upper()
        self.wst = raw_input("Have you passed WST? Please enter 'Y' or 'N': ").upper()

        while not(self.wst == "Y" or self.wst == "N"):
            self.wst = raw_input("Please enter 'Y' or 'N'. Have you passed WST? : ").upper()

        if self.wst == 'Y' or self.wst == 'N':
            if self.wst == 'Y':
                self.taken = True

        self.listOfClasses = self.user_input.split(",")
        requirement = requirements.Classes()

        for a_class in requirement.classes:
            x = requirement.classes[a_class].replace(" ", "").split(",")
            b = True
            print "checking class:",a_class
            for classes in x:
                if not(classes in self.listOfClasses):
                    b = False
                    break
            if b:
                print "Next sem you can take:",a_class

        print "you entered", self.listOfClasses
        print "User has passed WST", self.taken


user = Agent()
user.initial_question()
