import networkx as nx
import requirements
# import agents
from collections import defaultdict, deque
from collections import OrderedDict
from operator import itemgetter

class Graph(object):

    g = nx.DiGraph()
    requirement = requirements.Classes()
    #class_difficulty = agents.Agent().calculateDiff(agents.Agent().getFileData())

    """docstring for Graph."""
    def __init__(self):
        super(Graph, self).__init__()
        self.final_schedule = []
        self.listOfClasses = {}

        #create_weighted_graph()


    def create_weighted_graph(self, class_difficulty):
        requirement = requirements.Classes()

        self.g.add_edge("MATH19","MATH30", weight = round(class_difficulty['MATH19'] - class_difficulty["MATH30"],2))
        self.g.add_edge("MATH19","MATH42", weight = round(class_difficulty['MATH19'] - class_difficulty["MATH42"],2))
        self.g.add_edge("MATH19","CS46A", weight = round(class_difficulty['MATH19'] - class_difficulty["CS46A"],2))

        for cls in requirement.classes:
            prerequisite = requirement.classes[cls].replace(" ", "").split(",")
            for prereq in prerequisite:
                if prereq in class_difficulty and cls in class_difficulty:
                    difference = round(class_difficulty[cls] - class_difficulty[prereq],2)
                    self.g.add_edge(prereq, cls, weight = difference)
                else:
                    self.g.add_edge(prereq, cls)

    # list(bfs_paths(graph, 'A', 'F')) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
    def print_graph(self):
        requirement = requirements.Classes()
        print "The cls is Math19 "
        print self.g['MATH19']
        for cls in requirement.classes:
            print "The cls is %s " % (cls)
            print self.g[cls]
            print '\n'

    def BFS(self, G, source, classAvailable, num_of_cs_classes):
        visited = set()
        queue = [source]
        while queue:
            cls = queue.pop(0)
            if cls not in visited:
                visited.add(cls)
                queue.extend(self.turn_dict_into_set(G[cls]) - visited)
                print "The queue is: ", queue
                for cls2 in queue:
                    print "The cls2 is: ", cls2
                    print "The class available are: ", classAvailable
                    if cls2 in classAvailable and len(classAvailable) > 0:
                        if len(self.listOfClasses) < num_of_cs_classes:
                            print "The cls is: ", cls
                            if self.g.has_edge(cls, cls2):
                                print "Came here \n"
                                self.listOfClasses[cls2] = G[cls][cls2]['weight']
                                print "THe list of Classes are: ", self.listOfClasses
                                classAvailable.remove(cls2)
                        else:
                            sortedlists = sorted(self.listOfClasses.iterkeys(), key=lambda k: self.listOfClasses[k])
                            print " The sorted list is: ",sortedlists
                            self.update_list_of_classes(sortedlists, cls, cls2)
                            classAvailable.remove(cls2)

        for every_class in list(self.listOfClasses):
            self.final_schedule.append(every_class)
        return self.final_schedule


    """
    Turn a dict type object into a set.
    """
    def turn_dict_into_set(self, dict):
        newSet = set()
        for item in dict:
            newSet.add(item)
        return newSet

    # def update_list_of_classes(self, sortedlists, cls, cls2):
    #
    #     if self.g.has_edge(cls, cls2):
    #         current_weight = self.g[cls][cls2]['weight']
    #         for every_weight in list(self.listOfClasses):
    #             temp_weight = self.listOfClasses[every_weight]
    #             if current_weight > temp_weight:
    #                 self.listOfClasses[cls2] = self.g[cls][cls2]['weight']
    #                 del self.listOfClasses[every_weight]
    #                 print "The updated list is: ", self.listOfClasses
    #                 return


    def update_list_of_classes(self, sortedlists, cls, cls2):
            print "Came here \n"
            if self.g.has_edge(cls, cls2):
                current_weight = self.g[cls][cls2]['weight']
                for a_list in sortedlists:
                    temp_weight = self.listOfClasses[a_list]
                    print "The temp weight is: ", temp_weight
                    if current_weight > temp_weight:
                        self.listOfClasses[cls2] = current_weight
                        del self.listOfClasses[a_list]
                        print "The updated list is: ", self.listOfClasses
                        return



    # data = {1: 'b', 2: 'a'}
    # d = OrderedDict(sorted(data.items(), key=itemgetter(1), reverse=True))
    # print "D is: ", d
    #print BFS(g, 'CS46A', ['CS46B', 'CS146'], 1)
