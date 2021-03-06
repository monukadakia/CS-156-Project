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
                for cls2 in queue:
                    #print "Degree of %s is %d" % (cls,self.g.degree(cls))
                    if cls2 in classAvailable and len(classAvailable) > 0:
                        if len(self.listOfClasses) < num_of_cs_classes:
                            if self.g.has_edge(cls, cls2):
                                self.listOfClasses[cls2] = G[cls][cls2]['weight']
                                classAvailable.remove(cls2)
                        else:
                            sortedlists = sorted(self.listOfClasses.iterkeys(), key=lambda k: self.listOfClasses[k])
                            self.update_list_of_classes(sortedlists, cls, cls2)
                            classAvailable.remove(cls2)

        for every_class in list(self.listOfClasses):
            if not every_class in self.final_schedule:
                self.final_schedule.append(every_class)
        return self.final_schedule

    def BFS_graduation(self, G, source, classAvailable, num_of_cs_classes):

        graduation_classes = {}
        visited = set()
        queue = [source]

        while queue:
           cls = queue.pop(0)
           visited.add(cls)
           queue.extend(self.turn_dict_into_set(G[cls]) - visited)

           for cls2 in queue:
                if cls2 in classAvailable and len(classAvailable) > 0:
                    if len(graduation_classes) < num_of_cs_classes:
                        graduation_classes[cls2] = self.g.degree(cls2)
                        classAvailable.remove(cls2)
                    else:
                        sortedlists = sorted(graduation_classes.iterkeys(), key=lambda k: graduation_classes[k])
                        self.update_list_of_classes_grad(graduation_classes, sortedlists, cls2)
                        classAvailable.remove(cls2)
        final = []

        for every_class in list(graduation_classes):
                final.append(every_class)
        return final
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
            if self.g.has_edge(cls, cls2):
                current_weight = self.g[cls][cls2]['weight']
                for a_list in sortedlists:
                    temp_weight = self.listOfClasses[a_list]
                    if current_weight > temp_weight:
                        self.listOfClasses[cls2] = current_weight
                        del self.listOfClasses[a_list]
                        return

    def update_list_of_classes_grad(self, graduation_classes, sortedlists, cls2):
                current_degree = self.g.degree(cls2)
                for a_list in sortedlists:
                    temp_degree = self.g.degree(a_list)
                    if current_degree > temp_degree:
                        graduation_classes[cls2] = current_degree
                        del graduation_classes[a_list]
                        return

    # data = {1: 'b', 2: 'a'}
    # d = OrderedDict(sorted(data.items(), key=itemgetter(1), reverse=True))
    # print "D is: ", d
    #print BFS(g, 'CS46A', ['CS46B', 'CS146'], 1)
