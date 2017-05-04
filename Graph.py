import networkx as nx
import requirements

g = nx.DiGraph()
requirement = requirements.Classes()

for cls in requirement.classes:
    prerequisite = requirement.classes[cls].replace(" ", "").split(",")
    for prereq in prerequisite:
        g.add_edge(prereq, cls)


for cls in requirement.classes:
    print "The cls is %s " % (cls)
    print g[cls]
    print "\n"
