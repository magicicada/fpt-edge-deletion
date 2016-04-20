#!/usr/bin/env python

import EdgeDeletion as ed
import networkx as nx
import matplotlib.pyplot as plt
import graphFunctions as gf
import treeDecompositionForward as td
import JessDotParsing as jd
import EdgeDeletionForward as ed
import time
import sys



def printDelNice(delValues):
   for guy in delValues:
      print guy, " | ", delValues[guy]


def getChildren(tree, postorder, node):
    children = []
    nodeInd = postorder.index(node)
    neighbours  = tree.neighbors(node)
    for i in range(nodeInd):
        if postorder[i] in neighbours:
            children.append(postorder[i])
    return children
    

def forwardAlgorithm(graph, tree, root, h, k, orderOfComputation):
    delValuesTable = {}
    for guy in orderOfComputation:
        kind = tree.node[guy ]["kind"]
        delValuesThis = {}
        print "Processing node " + str(guy) + " which is kind " + str(kind)
        start = time.time()
        if kind =="LEAF":
            delValuesThis = td.get_del_values_leaf(graph, tree, guy, None, h, k)
            delValuesTable[guy] = delValuesThis
            
        elif kind == "FORGET":
            children = getChildren(tree, orderOfComputation, guy)
            delValuesThis = td.get_del_values_forget(graph, tree, guy, children, h, k, delValuesTable)
            delValuesTable[guy] = delValuesThis
            
        elif kind == "INTRODUCE":
            children = getChildren(tree, orderOfComputation, guy)
            delValuesThis = td.get_del_values_introduce(graph, tree, guy, children, h, k, delValuesTable)
            delValuesTable[guy] = delValuesThis
            
        else:# We must have a join
            children = getChildren(tree, orderOfComputation, guy)
            delValuesThis = td.get_del_values_join(graph, tree, guy, children, h, k, delValuesTable)
            delValuesTable[guy] = delValuesThis
        if delValuesThis == None or len(delValuesThis) == 0:
            print "No solution here, new detection method. Failed to make del values for " + str(guy)
            return None
        minDelValue = min(delValuesThis.values())
        if minDelValue == ed.INFINITY:
            print "No solution here."
            return None
        end = time.time()
        print "took time " + str(end-start) + " to find a number of del values " + str(len(delValuesThis))
    return delValuesTable



fileOfFiles = sys.argv[1]
# "singleFile"
baseFiles = []
for line in open(fileOfFiles):
    baseFiles.append(line.strip())
    

    
startString = "TreeDecomp"
endString = ".dgf.txt"

for baseFile in baseFiles:
    
    decompName = startString + baseFile + endString

    tree = jd.readDot(decompName)
    root = tree.nodes()[0]
    neighbours = tree.neighbors(root)
    td.make_it_nice(tree, root, neighbours)
    graph = gf.read_edges_from_file(baseFile, " ")

    
    root = tree.nodes()[0]
    tree = td.get_nice_tree_decomp(tree, root)
    orderOfComputation = list(nx.dfs_postorder_nodes(tree,root))
    
    delValuesTable = {}
    for guy in orderOfComputation:
         print str(guy)  +" has kind " + tree.node[guy ]["kind"] + " and bag " + tree.node[guy ]["label"] + " and neighbours " + str(tree.neighbors(guy))

    maxK = len(graph.edges())
    maxH = 6
    hSolved = False
    start1 = time.time()
    for h in range(5, maxH):
        for k in range(6, maxK):
            start = time.time()
            print "Testing at " + str(k) + " removals " + " for component of size " + str(h)
            delValuesTable = forwardAlgorithm(graph, tree, root, h, k, orderOfComputation)
            if delValuesTable != None:
                print "Solution found at " + str(k) + " removals " + " for component of size " + str(h)
            end = time.time()
            if delValuesTable != None:
              print "Solution! Elapsed time for h = " + str(h) + " and k = " + str(k) + " is " + str(end - start) + " file " + baseFile
              end1 = time.time()
              print "TABLERESULT," + baseFile + "," + str(h) + "," + str(k) + "," + str(end1 - start1)
              hSolved = True
              
              break
            else: 
              print "No! Elapsed time for h = " + str(h) + " and k = " + str(k) + " is " + str(end - start) + " file " + baseFile
            sys.stdout.flush()
            

