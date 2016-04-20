#!/usr/bin/env python
import networkx as nx

# The hackiest version of this ever made
#  We need to get the bags and the edges 
def readDot(filename):
    graph = nx.Graph()
    bags = {}
    for line in open(filename):
        if "label" not in line:
            if "--" in line: #then we have an edge
                split = line.strip().split()
                if split[1] != "--":
                    print "warning, problem aparsing edge line " + line.strip()
                else:
                    graph.add_edge(split[0], split[2])
        else: # then we have a label
            firstSplit = line.strip().split()
            node = firstSplit[0]
            if node in bags:
                print "warning! overwriting bag list for " + node
            # print "first split for line " + line.strip() + " is " + str(firstSplit)
            justBag = line.split("\"")[1]
            # print "just bag " + str(justBag) 
            bags[node] = justBag.strip().split()
            graph.add_node(node)
            graph.node[node]["label"] = justBag.strip()
    return graph        
    
    # print graph.edges()
    # for guy in bags:
    #     print guy + "  " + str(bags[guy])
            

    
