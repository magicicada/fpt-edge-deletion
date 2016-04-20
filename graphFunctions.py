import networkx as nx

# Reads in edges from a file. The edges are stored in
# tuples, one tuple per line. Each tuple holds the numbers
# of the two vertices at the endpoints of the edge that the
# tuple represents.
# Input - the filename of the file holding the data for the edges
#       - the delimiter between the two vertices i.e. ",", "-" or " ", etc.
# Output - a graph object with all of the vertices and edges.
def read_edges_from_file(filename, delimiter):
    f = open(filename, "r")
    graph = nx.Graph()
    currentLine = f.readline()
    while(currentLine != ""):
        # Remove unwanted characters and add in the new edge
        cleanedLine = currentLine.strip().split(delimiter)
        firstVertex = cleanedLine[0]
        secondVertex = cleanedLine[1]
        graph.add_edge(firstVertex,secondVertex)
        currentLine = f.readline()
    f.close()
    return graph

# Calculates the maximum size of a component in a graph
# Input - a graph object
# Output - an integer number; the maximum component size
def maximum_component_size(graph):
    maximum = 0
    # Loop over all components to find maximum
    for component in nx.connected_components(graph):
        if len(component) > maximum:
            maximum = len(component)
    return maximum

# Checks whether the maximum component size is less than a given number
# Input - a graph object and an integer to check against
# Output - a boolean value:
#     True -> the maximum component size is less than or equal to the number
#     False -> the maximum component size is more than the number
def maximum_at_most(graph, comp_size_limit):
    maximum = maximum_component_size(graph)
    return maximum <= comp_size_limit

# Checks if a given set of edges of a graph disconnect the graph into
# components of some maximum size. No changes to the original graph are made.
# Input - a graph object, an integer to check against and a set of edges to delete
# Output - a boolean value:
#     True -> the maximum component size is less than or equal to the number
#     False -> the maximum component size is more than the number
def is_edge_set_disconnecting(graph, comp_size_limit, edges):
    # Create a copy to preserve original graph
    graph_copy = graph.copy()
    # Remove all edges in the set of edges
    for edge in edges:
        graph_copy.remove_edge(edge[0], edge[1])
    # Check if condition has been satisfied
    return maximum_at_most(graph_copy, comp_size_limit)

# Checks if the graph composed of a given set of edges and the vertices
# they connect form a graph of component size less than a given number
# Input - an integer to check against and a set of edges to form the graph
# Output - a boolean value:
#     True -> the maximum component size is less than or equal to the number
#     False -> the maximum component size is more than the number
def is_edge_set_disconnected(comp_size_limit, edges):
    # Create a new empty graph
    graph = nx.Graph()
    # Add the given edges to the new graph
    for edge in edges:
        graph.add_edge(edge[0],edge[1])
    # Check what the maximum component size is
    return maximum_at_most(graph, comp_size_limit)

def find_degrees_of_end_vertices(given_edge, all_edges):
    degrees = [0,0]
    for i in range(1):
        vetrex = given_edge[i]
        other_vertex = given_edge[1-i]
        for edge in all_edges:
            if edge[0] == vetrex or edge[1] == vertex:
                degrees[i] += 1
    return degrees

def min_degree_of_end_vertices(given_edge, all_edges):
    degrees = find_degrees_of_end_vertices(given_edge, all_edges)
    if degrees[0] < degrees[1]:
        return degrees[0]
    else:
        return degrees[1]

def average_degree_of_end_vertices(given_edge, all_edges):
    degrees = find_degrees_of_end_vertices(given_edge, all_edges)
    return (degrees[0] + degrees[1]) /2
