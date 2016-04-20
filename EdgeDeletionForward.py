#!/usr/bin/env python

import sys
import copy
import networkx as nx
from collections import Counter
import itertools


INFINITY = 999999999

# I've given up, and am just going to start re-writing things. 

# this is just a hack for now.  Friday 1st April.
# it will store the del values with partitions for node v16, and we'll see if that
# helps with computation time for node 84 
scratchStorage = {}

def noBigSteps(candidate):
    sortV =sorted(candidate)
    # A check to make sure no duplicates are allowed
    if 1 not in candidate:
        return False
    for i in range(0, len(sortV) - 1):
        if sortV[i+1] - sortV[i] > 1:
            # print "" 
            # print "=========================="
            # print "candidate failing!"
            # print candidate
            # print "=========================="
            # print "" 
            return False
    return True

def nextPartition(current, maxH, size):
    # first do sanity check for done
    #last = True
    # print "considering current "
    # print current
    #for i in range(0, len(current)-1):
    #    if current[i+1] != current[i]+1:
            # print "not found to be the last"
    #        last = False
    # print "the last check value is " + str(last)
    # print "the first val check value is " + str(current[0] == 1)
    #if last and current[0] == 1:
    #    return "DONE"
    
    newPartition = []
    canDo = False
    for guy in current:
        newPartition.append(guy)
    if current[len(current)-1] < size:
       newPartition[len(newPartition)-1] = newPartition[len(newPartition)-1] + 1
    else:
#         the below should maybe be: (len(newPartition)-2, -1, -1): 
        for i in range(len(newPartition)-2, -1, -1):
            if newPartition[i] < size:
                canDo = True
                newPartition[i] = newPartition[i] + 1
                for j in range(i+1, len(newPartition)):
                    newPartition[j] = 1
                break
        if not canDo: ##
            newPartition = "DONE"
    # print newPartition
    return newPartition

# generate all partitions of guys in bag such that
# no partition is larger than maxH
# currently returns integer list encoding.  Is that adequate?
def getAllPartitions(bag, maxH):
    size = len(bag)
    partitions = []
    # now we want all numbers up to 1,2,3,4,... using only the digits 1 to size
    #  and really, we don't want more than maxH of any single digit
    # never use a digit that?s more than 1 larger than any other digit in the encoding
    firstPartition = [1] * size
    currentPartition = firstPartition
    while currentPartition != "DONE":
        partitions.append(currentPartition)
        currentPartition = nextPartition(currentPartition, maxH, size)
    # print "partitions= ",partitions
    goodPartitions = []
    for guy in partitions:
        # print ">", guy
        #guy = sorted(guy)
        if guy not in goodPartitions and max(Counter(guy).values())<= maxH:
            # print "=>", guy
            if noBigSteps(guy):
                goodPartitions.append(guy)
                # print guy
    return goodPartitions

# print getAllPartitions([1,2,3,4],3)

# changes numerical partition encodings into actual bags
# I'm not checking to see if the partitions are valid, yet
# will return a list of lists of lists    #added a weak validity check
def bagEm(partitionList, bag):
    partitioned = []
    for guy in partitionList:
        dictOfParts = {}
        for i in range(0, len(guy)):
            if guy[i] not in dictOfParts:
                dictOfParts[guy[i]] = []
            dictOfParts[guy[i]].append(bag[i])
        if sorted(dictOfParts.values()) not in partitioned:
            partitioned.append(sorted(map(sorted,dictOfParts.values())))
    return partitioned

# print bagEm(getAllPartitions([1, 2, 3, 4], 4), [1, 2, 3, 4])

# A weak validity check for unbagged partition lists
# Should prevent double counting.
def partition_not_repeating(partitionList):
    pass

def nextFunction(current, maxVal):
    if len(current) == 0:
        print "WARNING: LENGTH OF CURRENT FUNCTION IS ZERO"
    newPartition = []
    canDo = False
    for guy in current:
        newPartition.append(guy)
    if current[len(current)-1] < maxVal:
       newPartition[len(newPartition)-1] = newPartition[len(newPartition)-1] + 1
    else:
#         the below should maybe be: (len(newPartition)-2, -1, -1): 
        for i in range(len(newPartition)-2, -1, -1):
            if newPartition[i] < maxVal:
                canDo = True
                newPartition[i] = newPartition[i] + 1
                for j in range(i+1, len(newPartition)):
                    newPartition[j] = 1
                break
        if not canDo:
            newPartition = "DONE"
    # print "RETURNING A NEW PARTITION OF " + str( newPartition)
    return newPartition

def getAllFunctionsLeaf(partition, maxH):
    # print "New call of function"
    # print "generating functions for: "
    allFunctions = []
    guy = partition
    # for guy in partitions:
    # print "Now working on partition "
    # print guy
    # print "who has length " + str(len(guy))
    firstFunction = [1] * len(guy)

    # print "first function is " + str(firstFunction)
    currentFunction = firstFunction
    while currentFunction != "DONE":
        # if currentFunction == "DONE":
        #         break
        # print "at top of while, the current function is " + str(currentFunction)
        if currentFunction != "DONE":
            # print "at top of if, the current function is " + str(currentFunction)
            #print "check validity of " + str(currentFunction) + " for " + str(guy)
            isValid = True
            for i in range(0, len(currentFunction)):
                # print "comparing " + str(currentFunction[i]) + " to " + str(len(guy[i]))
                if currentFunction[i] != len(partition[i]):
                    isValid = False
            if isValid:
                #print "ADDED!!"
                dictThis = {}
                for i in range(0, len(currentFunction)):
                    dictThis[tuple(partition[i])] = currentFunction[i]
                allFunctions.append(dictThis)
            # print "On line 166, the current function is " + str(currentFunction)
            currentFunction = nextFunction(currentFunction, maxH)
            # if currentFunction == "DONE":
            #     print "inside test, breaking, the current function is " + str(currentFunction)
            #     break
            # print "On line 168, the current function is " + str(currentFunction)
            # print "all functions is " + str(allFunctions)
        # if currentFunction == "DONE":
        #         print "inside second test, breaking, the current function is " + str(currentFunction)
        #         break
        # if currentFunction == []:
        #         print "inside third test, breaking, the current function is " + str(currentFunction)
        #         break
        # print "At end of loop, current function is " + str(currentFunction)
        #print " a possible function " + str(currentFunction)
    #print "done generating functions"
    return allFunctions 


# will give functions as dictionaries, in a list
def getAllFunctions(partition, maxH):
    # print "New call of function"
    # print "generating functions for: "
    allFunctions = []
    guy = partition
    # for guy in partitions:
    # print "Now working on partition "
    # print guy
    # print "who has length " + str(len(guy))
    firstFunction = [1] * len(guy)

    # print "first function is " + str(firstFunction)
    currentFunction = firstFunction
    while currentFunction != "DONE":
        # if currentFunction == "DONE":
        #         break
        # print "at top of while, the current function is " + str(currentFunction)
        if currentFunction != "DONE":
            # print "at top of if, the current function is " + str(currentFunction)
            #print "check validity of " + str(currentFunction) + " for " + str(guy)
            isValid = True
            for i in range(0, len(currentFunction)):
                # print "comparing " + str(currentFunction[i]) + " to " + str(len(guy[i]))
                if currentFunction[i] < len(partition[i]):
                    isValid = False
            if isValid:
                #print "ADDED!!"
                dictThis = {}
                for i in range(0, len(currentFunction)):
                    dictThis[tuple(partition[i])] = currentFunction[i]
                allFunctions.append(dictThis)
            # print "On line 166, the current function is " + str(currentFunction)
            currentFunction = nextFunction(currentFunction, maxH)
            # if currentFunction == "DONE":
            #     print "inside test, breaking, the current function is " + str(currentFunction)
            #     break
            # print "On line 168, the current function is " + str(currentFunction)
            # print "all functions is " + str(allFunctions)
        # if currentFunction == "DONE":
        #         print "inside second test, breaking, the current function is " + str(currentFunction)
        #         break
        # if currentFunction == []:
        #         print "inside third test, breaking, the current function is " + str(currentFunction)
        #         break
        # print "At end of loop, current function is " + str(currentFunction)
        #print " a possible function " + str(currentFunction)
    #print "done generating functions"
    return allFunctions 

# print getAllFunctions([[1,2],[3,4]], 3)
def printSignatureNicely(sig):
    (partition, function) = sig
    return "Partition P:  " + str(partition) + " Function c: " + str(function)
    

def generateAllStates(t, treeDecomp, bag, graph, h):
    # print "Generating all states for " + str(bag)
    states = []
    allP = getAllPartitions(bag, h)
    # print "========partitions of bag =============="
    # print bag
    # for guy in allP:
    #     print guy
    # print "================================"
    allPartitions  = bagEm(allP, bag)
    # print allPartitions
    # allPartitions = [[allPartitions[3]]]
    for p in allPartitions:
        
        # print "p=", p, "h=", h
        allFunctions = getAllFunctions(p, h)
        # print "all functions is"
        # print allFunctions
        for c in allFunctions:
             states.append((p, c))
             # print "appending state " + printSignatureNicely((p, c))
    # print "Finished generating all states"
    # for state in states:
        # print "A State! : " + printSignatureNicely(state)
    return states

def generateAllStatesLeaf(t, treeDecomp, bag, graph, h):
    # print "Generating all states for " + str(bag)
    states = []
    allP = getAllPartitions(bag, h)
    # print "========partitions of bag =============="
    # print bag
    # for guy in allP:
    #     print guy
    # print "================================"
    allPartitions  = bagEm(allP, bag)
    # print allPartitions
    # allPartitions = [[allPartitions[3]]]
    for p in allPartitions:
        
        # print "p=", p, "h=", h
        allFunctions = getAllFunctionsLeaf(p, h)
        # print "all functions is"
        # print allFunctions
        for c in allFunctions:
             states.append((p, c))
             # print "appending state " + printSignatureNicely((p, c))
    # print "Finished generating all states"
    # for state in states:
        # print "A State! : " + printSignatureNicely(state)
    return states

# print generateAllStates(None,:w

def inSamePart(partition, u, v):
    for guy in partition:
        if u in guy and v in guy:
            return True
    #print "checking partition spans, found " + str(u)+ "-" + str(v) + " are not in the same part of " + str(partition)
    return False

# Number of things not contained in any one given partition
def countSpans(graph, bag, partition):
    subgraph = graph.subgraph(bag)
    count = 0
    for (u, v) in subgraph.edges():
        if not inSamePart(partition, u, v):
            count = count + 1
    return count

# The number of edges adjacent to v that do not connect v to nodes in the same partition
def countSpansSingle(graph, bag, partition, v):
    subgraph = graph.subgraph(bag)
    count = 0
    for u in subgraph.neighbors(v):
        # print "considering whether edge " + str(u) + " and " + str(v) + " needs counting "
        if not inSamePart(partition, u, v):
            # print " it does, as they're not in the same part of  "  + str(partition)
            count = count + 1

    return count

def sorted_dictionary_to_string(dictionary):
    keys = sorted(dictionary.keys())
    string = ""
    for key in keys:
        string = string + str(sorted(key)) + ": " + str(dictionary[key]) + ", "
    return "{" + string[:-2] + "}"
    
def sigOfLeaf(t, treeDecomp, bag, graph, h, k):
    delValues = {}
    #print "Generating states"
    allStates = generateAllStatesLeaf(t, treeDecomp, bag, graph, h)
    actualStates = []
    #print "considering each state" # Here
    for (p, c) in allStates:
        subgraph = graph.subgraph(bag) # Move this
        #print "-counting spanning edges within " + str(bag)
        #print " for parition " + str(p)
        #print " and for func " + str(c)
        countEdges = countSpans(graph, bag, p) # Pass only subgraph
        # print "FOR PARTITION " + str(p) + " counted edges is " + str(countEdges)
        #print " count is " + str (countEdges)
        
        if countEdges <= k:
            delValues[(str(p), sorted_dictionary_to_string(c))] = countEdges
            actualStates.append((p, c))
            
        # else:
            # delValues[(str(p), sorted_dictionary_to_string(c))] = INFINITY
    print "storing del values for " + str(t) + " explicitly"
    scratchStorage[t] = actualStates
    return delValues
# G = nx.Graph()
# G.add_edge(1,2)
# G.add_edge(3,2)
# G.add_edge(3,4)
# print sigOfLeaf(None, None, [1,2,3,4], G, 3, 2)


# def givenSigsGetDelLeaf(t, treeDecomp, bag, graph, h, k, sigs):
#     for (p, c) in sigs:
        

def generateAllRefinements(part, v, h):
    #print "in generateAllRef, we've received " + str(part)
    if part == [v]:
        return []
    toPartition = [x for x in part if x != v]
    #print "in generateAllRef, we need to partition " + str(toPartition)
    return bagEm(getAllPartitions(toPartition, h), toPartition)

# print generateAllRefinements([1,2,3,4],3,3)

from itertools import chain, combinations
def powerset(iterable):
  xs = list(iterable)
  # note we return an iterator rather than a list
  return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )



def sigOfIntroduce(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h, k):
    if bag == childBag:
        print "WARNING: False introduce found "
        scratchStorage[t] = scratchStorage[childT]
        return delValuesChild
    
    delValues  = {}
    actualStates = []
    if len(delValuesChild) == 0:
        return delValues
#     we'll do a sanity check
    parentNotChild = list(set(bag) - set(childBag))
    childNotParent = list(set(childBag) - set(bag))
    if len(parentNotChild) != 1:
        print "WARNING: introduce node does not have one more than its child"
    if len(childNotParent) != 0:
        print "WARNING: child node has a guy not in its introduce parent"
    
    v = list(set(bag) - set(childBag))[0]
    allStates = []
#     this is an effort at speedup by iterating over child legal states
    print "child is " + str(childT)
    if childT in scratchStorage:
        print "Using the shortcut to introduce states"
        parentStates = []
        for (p, c) in scratchStorage[childT]:
            # we'll produce a new state by adding v to each combination of bags
            childSigString = str(sorted(map(sorted,p))), sorted_dictionary_to_string(c)
            childDel = delValuesChild[childSigString]
            
            for subset in powerset(p):
                # print "considering subset " + str(subset) + " from child partition " + str(p)
                newPart = list(set().union(*subset))
                if len(newPart) < h:
                    newPart = newPart + [v]
                    parentPart = [newPart]
                    parentC = {}
                    XrC = 0
                    for childPart in subset:
                        XrC = XrC + c[tuple(childPart)]
                    parentC[tuple(newPart)] = XrC +1
                    
                    for childPart in p:
                        if childPart not in subset:
                            parentPart.append(childPart)
                            parentC[tuple(childPart)] = c[tuple(childPart)]
                    value = childDel + countSpansSingle(graph, bag, parentPart, v)
                    if value <= k and max(parentC.values()) <= h:
                        # print "We will add value of " + str(value) + " because it is at most "  + str(k)
                        if (parentPart, parentC) not in parentStates:
                            parentStates.append((parentPart, parentC))
                        if (parentPart, parentC)  not in actualStates:
                            actualStates.append((parentPart, parentC))
                        # now we'll go about getting the del values for this state
                        
                        
                        parentString = (str(sorted(map(sorted,parentPart))), sorted_dictionary_to_string(parentC))
                        if parentString not in delValues or value < delValues[parentString]:
                            delValues[parentString] = value
                    
            
            
# #             This is like the combination of only one child partition
#             for part in p:
#                 if len(part) < h:
#                     newPart = part + [v]
#                     parentPart = [newPart]
#                     parentC = {}
#                     parentC[tuple(newPart)] = c[tuple(part)] +1
#                     for childPart in p:
#                         if childPart != part:
#                             parentPart.append(childPart)
#                             parentC[tuple(childPart)] = c[tuple(childPart)]
#                 
#                     parentStates.append((parentPart, parentC))
#                     # now we'll go about getting the del values for this state
#                     value = childDel + countSpansSingle(graph, bag, newPart, v)
#                     delValues[(str(sorted(map(sorted,parentPart))), sorted_dictionary_to_string(parentC))] = value
        print "storing del values for " + str(t) + " explicitly"
        scratchStorage[t] = actualStates              
        return delValues           

                   
#       by this point we should have parent statesand del values?
                    
                    
                    
    
    
    # print "doing the introduce node"
    #print "calculating v"
    
    # print "The introduced node is " + str(v)
    #print "calculating all states"
    else:
        print "using the old introduce method"
        allStates = generateAllStates(t, treeDecomp, bag, graph, h)
        #print "for each guy in allStates"
        # print "starting iteration over allStates"
        for (p, c) in allStates:
            # print "top of iteration loop " + str((p, c))
            # generating the inherited states
            # print "==========considering " + str((p, c)) + " from allStates========"
            inherited = []
            Xr = []
            # print "looking for Xr"
            for dude in p:
                if v in dude:
                    Xr  = dude
            # print "Xr is " + str(Xr)
            if Xr == []:
                print "problem: cannot find a partition containing v in introduce procedure"
            # Generate refinements
            remainderP = copy.deepcopy(p)
            remainderP.remove(Xr)
            # print "remainderP is " + str(remainderP)
            # print "Generating refinements"
            refinements  =  generateAllRefinements(Xr, v, h)
            # print "for each refinement of "
            # print refinements
    #         MISSING CASE WHERE NO REFINEMENTS _ REMOVES AN ENTIRE COMP!
            # this is a hack to avoid missing out the situation with an empty partition
            # 
            if len(Xr) == 1:
                refinements.append([])
            for refinedPart in refinements: # for refinement in refinements?
                # print "for refinedPart " + str(refinedPart)
    #             added below line on March 23rd LEFTOFF
                pPrime = remainderP
    #             what about a case when there's only empty refinements.  That seems wrong.
                if refinedPart != []:
                    pPrime = remainderP + refinedPart # P'
                allRefinedFunctions = getAllFunctions(sorted(pPrime), h)
                # print "all refined functions is "+ str (allRefinedFunctions)
                for guy in allRefinedFunctions: # This is no longer in pseudocode, on purpose?
                    # print "now to check the sum condition in " + str(guy)
                    # check sum condition: error in pseudocode here?TODO
                    sumOf = 0
                    if refinedPart == []: 
                        # print "The c is " + str(c[tuple(Xr)])
    #                    right now this allows any sort of c value on a $X_r$, provided that the introduced vertex is the only thing in that partition
                        inherited.append((sorted(pPrime), guy))
                    else:
                        for entry in refinedPart:
                            #print "adding in the function for " + str(entry) + " which is " + str(guy[tuple(entry)])
                            sumOf = sumOf + guy[tuple(entry)]
                        # print "total sum is " + str(sumOf)
                        # print "which we will compare to " + str(c[tuple(Xr)]-1)
                        if sumOf == c[tuple(Xr)]-1:
                            inherited.append((sorted(pPrime), guy))
            # print "for state " + str((p, c)) + " the inherited list is "
            # print str(inherited)
            minValue = INFINITY
            # print "inherited set found"
            for (pPrime, cPrime) in inherited: # t' no longer used?
                # print "looking at " + str((pPrime, cPrime)) + " in inherited"
                # print "the del values are"
                # # print "del values for child are "
                # # print str(delValuesChild)
                # print delValuesChild[(str(pPrime), sorted_dictionary_to_string(cPrime))]
                # print "the child del values are "
                # for guy in delValuesChild:
                #     print str(guy) + "  " + str(delValuesChild[guy])
                
                sigString = (str(sorted(map(sorted,pPrime))), sorted_dictionary_to_string(cPrime))
                if sigString in delValuesChild:
                    value = delValuesChild[sigString] + countSpansSingle(graph, bag, p, v)
                    if value < minValue:
                        minValue = value
                    
                        # print "We've found a (introduce) value of " + str(value) + " for " + printSignatureNicely((p, c))
                        # print "from the inherited value of " + str(delValuesChild[(str(sorted(map(sorted,pPrime))), sorted_dictionary_to_string(cPrime))]) + " for "+ printSignatureNicely((pPrime, cPrime))
                        # print "with countspans of " + str(countSpansSingle(graph, bag, pPrime, v))
    
            if minValue <= k:
                delValues[(str(sorted(map(sorted,p))), sorted_dictionary_to_string(c))] = minValue
            # else:
        #     delValues[(str(sorted(map(sorted,p))), sorted_dictionary_to_string(c))] = INFINITY
    return delValues

def is_function_valid(c):
    valid = True
    for Xr in c:
        if c[Xr] < len(Xr):
            valid = False
    return valid

def sigOfForget(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h, k):
    print "child is " + str(childT)
    delValues  = {}
    actualStates = []
    if len(delValuesChild) == 0:
        return delValues
    
    diff = list(set(childBag) - set(bag))
    if len(diff) != 1:
        print "Warning! Forget node bag does not differ from child by one member"
        print diff
    v = diff[0]
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    #print "Allstates = ", allStates
    inheritedSets = []
    for (p, c) in allStates:
#     generating the inherited sigma set
        inheritedPartitions = []
        # make a bunch of copies, one for v being added to each part
        for part in p:
            if len(part) < h:
                newPart = []
                for secondPart in p:
                    if secondPart != part:
                        newPart.append(copy.deepcopy(secondPart))
                    else:
                        newPart.append(copy.deepcopy(secondPart) + [v])
                inheritedPartitions.append(map(sorted,newPart))
        # add it in its own part
        temp = copy.deepcopy(p)
        temp.append([v])
        inheritedPartitions.append(map(sorted,temp))
        

        #print "inherited = ", inheritedPartitions
        #print "THIS IS " + printSignatureNicely((p, c))
        
        
        inheritedSets = []
        for pPrime in inheritedPartitions:
            #print "pprime=", pPrime
            allCPrime = []
            cPrime = {}
            vSingleton = False
            for part in pPrime:
                if part != [v]:
                    #print "part= ", copy.deepcopy(part)
                    #print "v= ", v
                    partWithoutV = copy.deepcopy(part)
                    if v in partWithoutV:
                        #print "v in partwithoutV"
                        partWithoutV.remove(v)
                    #print "partwithoutV= ",partWithoutV
                    #print "cc=", c
                    #print "c=",c[tuple(partWithoutV)]
                    cPrime[tuple(part)] = c[tuple(partWithoutV)] #it is possible to get incorrect fnc here?
                    #print "cp=", cPrime
                else:
                    vSingleton = True
            if not vSingleton:
                allCPrime.append(cPrime)
            else:
                for i in range(h+1):
                    if i <= h and i >= 1:
                        newCPrime = copy.deepcopy(cPrime)
                        newCPrime[tuple([v])] = i
                        allCPrime.append(newCPrime)
            
            for cPrime in allCPrime:
                #print "cprime", cPrime
                if is_function_valid(cPrime):
                    inheritedSets.append((pPrime,cPrime))
                #else:
                    #print "State not valid: ", pPrime, cPrime

        minValue = INFINITY
        
        
        for (pPrime, cPrime) in inheritedSets:
            #print "pPrime", pPrime, "cPrime", cPrime
            if (str(sorted(map(sorted,pPrime))),sorted_dictionary_to_string(cPrime)) not in delValuesChild:
                # print "Warning! Child state not found in forget."
                x = 1
            else:
                # print "At least one child state found in forget"
                childString = str(sorted(map(sorted,pPrime))),sorted_dictionary_to_string(cPrime)
                if childString in delValuesChild:
                    value = delValuesChild[childString]
                
                    if value < minValue:
                        #print "We've found a value of " + str(value) + " for " + printSignatureNicely((pPrime, cPrime))
                        minValue = value

        if minValue <= k:
            delValues[str(sorted(map(sorted,p))),sorted_dictionary_to_string(c)] = minValue
            if (p, c) not in actualStates:
                actualStates.append((p, c))
        # else:
        #     delValues[str(sorted(map(sorted,p))),sorted_dictionary_to_string(c)] = INFINITY
    print "storing del values for " + str(t) + " explicitly"
    scratchStorage[t] = actualStates 
    return delValues
            
#             MAYBE COMPLETED


def sigOfJoin(t, treeDecomp, bag, graph, childT1, childT2, childBag1, childBag2, delValuesChild1, delValuesChild2, h, k):
    delValues = {} #     delValues  = {}
    actualStates = []
    if len(delValuesChild1) == 0 or len(delValuesChild2) == 0:
        return delValues
    allStates = []
    print "children are " + str(childT1) + " and " + str(childT2)
    if childT1 in scratchStorage and childT2 in scratchStorage:
        print "using the join shortcut"
        child1States = scratchStorage[childT1]
        child2States = scratchStorage[childT2]
        for (p1, c1) in child1States:
            for (p2, c2) in child2States:
                if str(sorted(p1)) == str(sorted(p2)):
                    # slightly worried about this comparison of lists of lists
                    # print "we've found two equal partitions: "
                    parentPartition = copy.deepcopy(p1)
                    parentC = {}
                    for part in parentPartition:
                        parentC[tuple(part)] = c1[tuple(part)] + c2[tuple(part)] - len(part)
                        
                    childString1 = str(sorted(map(sorted,p1))),sorted_dictionary_to_string(c1)
                    childString2 = str(sorted(map(sorted,p2))),sorted_dictionary_to_string(c2)
                    parentString = str(sorted(map(sorted,parentPartition))),sorted_dictionary_to_string(parentC)
                    value = delValuesChild1[childString1] + delValuesChild2[childString2] - countSpans(graph, bag, parentPartition)
                    if value <= k and max(parentC.values()) <= h:
                        
                        if (parentPartition, parentC) not in allStates:
                            allStates.append((parentPartition, parentC))
                            delValues[parentString] = value
                        if (parentPartition, parentC) not in actualStates:
                            actualStates.append((parentPartition, parentC))
                        if delValues[parentString] > value:
                            delValues[parentString] = value
        
        print "storing del values for " + str(t) + " explicitly"
        scratchStorage[t] = actualStates             
        return delValues
    
    
    
    else:
        print "using the old join method "
        allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    
        for (p,c) in allStates:
            # generating the inherited join states
            inheritedStates = []
            p1 = copy.deepcopy(p)
            p2 = copy.deepcopy(p)
            # generate all function pairs
            allFunctionPairs = []
            allRefinedFunctions = getAllFunctions(p1, h)
            for c1 in allRefinedFunctions:
                for c2 in allRefinedFunctions:
                    for blockX in p:
                        if c[tuple(blockX)] == c1[tuple(blockX)] + c2[tuple(blockX)] - len(blockX):
                            allFunctionPairs.append((c1,c2))
            
            # add state to inherited states
            for (c1, c2) in allFunctionPairs:
                inheritedStates.append(((p1,c1),(p2,c2)))
    
            minValue = INFINITY
            for ((p1,c1),(p2,c2)) in inheritedStates:
                #print "1 del1=", delValuesChild1[str(p1), sorted_dictionary_to_string(c1)]
                #print "2 del2=", delValuesChild2[str(p2),sorted_dictionary_to_string(c2)]
                childString1 = str(sorted(map(sorted,p1))), sorted_dictionary_to_string(c1)
                childString2 = str(sorted(map(sorted,p2))),sorted_dictionary_to_string(c2)
                if childString1 in delValuesChild1 and childString2 in delValuesChild2:
                    value = delValuesChild1[childString1] + delValuesChild2[childString2] - countSpans(graph, bag, p)
                    if value < minValue:
                        minValue = value
    
            if minValue <= k:
                delValues[(str(sorted(map(sorted,p))),sorted_dictionary_to_string(c))] = minValue
            # else:
            #     delValues[(str(sorted(map(sorted,p))),sorted_dictionary_to_string(c))] = INFINITY
                
        return delValues



# tree = nx.Graph()
# tree.add_edge('a', 'b')
# tree.add_edge('b', 'c')
# tree.add_edge('c', 'd')
# tree.add_edge('c', 'e')
# bags = {}
# bags['a'] = [2, 3, 4, 5]
# bags['b'] = [2, 3, 4]
# bags['c'] = [1, 2, 3, 4]
# bags['d'] = [1, 2, 3, 4]
# bags['e'] = [1, 2, 3, 4]
# 
# graph = nx.Graph()
# graph.add_edge(5, 3)
# graph.add_edge(2, 3)
# graph.add_edge(1, 3)
# graph.add_edge(1, 2)
# graph.add_edge(1, 4)
# #graph.add_edge(1, 2)
# #graph.add_edge(2, 3)
# #graph.add_edge(3, 4)
# #graph.add_edge(4, 5)
# 
# 
# h = 2
# k = 3
# 
# leafOrder = ['d', 'e', 'c', 'b', 'a']
# def fakeMethod():
# # testing the nice tree decomp generator
#     import treeDecomposition as td
#     td.printArb()
# 
# fakeMethod()
# niceOne = td.get_nice_tree_decomp(tree, "a")
# print niceOne


# generateAllStates(1, 2, [1, 2, 3, 4], graph, h)

# #NONSENSE = "nonsense"
# delValuesLeafD = sigOfLeaf(tree, bags, bags['d'], graph, h, k)
# delValuesLeafE = sigOfLeaf(tree, bags, bags['e'], graph, h, k)
# for guy in delValuesLeafD:
#     if delValuesLeafD[guy] < INFINITY:
#      print printSignatureNicely(guy) + " maps to " + str(delValuesLeafD[guy])
#     
# # del values for the join node
# delValuesC = sigOfJoin('c', tree, bags['c'], graph, 'd', 'e', bags['d'], bags['e'], delValuesLeafD, delValuesLeafE, h, k)
# for guy in delValuesC:
#     if delValuesC[guy] < INFINITY:
#        print printSignatureNicely(guy) + " maps to " + str(delValuesC[guy])
# 
# 
# # del values for the forget node
# delValuesB = sigOfForget('b', tree, bags['b'], graph, 'c', bags['c'], delValuesC, h, k)
# for guy in delValuesB:
#     if delValuesB[guy] < INFINITY:
#        print printSignatureNicely(guy) + " maps to " + str(delValuesB[guy])
# 
# 
# # del values for the introduce node
# 
# print "Calculating for introduce node:"
# delValuesA = sigOfIntroduce('a', tree, bags['a'], graph, 'b', bags['b'], delValuesB, h, k)
# for guy in delValuesA:
#     if delValuesA[guy] < INFINITY:
#        print printSignatureNicely(guy) + " maps to " + str(delValuesA[guy])



    
#delValuesLeaf2 = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3,4], graph, h, k)
#print "+++++++FOR LEAF++++++++"
#for guy in delValuesLeaf:
#    print str(guy) + " | " + str(delValuesLeaf[guy])
#delValuesIntr = sigOfIntroduce(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, [1,2,3], delValuesLeaf, h, k)
#print "+++++++Introduce++++++++"
#for guy in delValuesIntr:
#    if delValuesIntr[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesIntr[guy])
#delValuesForget = sigOfForget(NONSENSE, NONSENSE, [1,3,4], graph, NONSENSE, [1,2,3,4], delValuesLeaf, h, k)
#print "+++++++Forget++++++++"
#for guy in delValuesForget:
#    if delValuesForget[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesForget[guy])
#delValuesJoin = sigOfJoin(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, NONSENSE, NONSENSE, NONSENSE, delValuesIntr, delValuesLeaf2, h, k)
#print "+++++++Join++++++++"
#for guy in delValuesJoin:
#    if delValuesJoin[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesJoin[guy])

