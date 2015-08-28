import re, sys, math, random, csv, types, networkx as nx
from collections import defaultdict

def parse(filename, isDirected):
    reader = csv.reader(open(filename, 'r'), delimiter=',')
    next(reader)
    data = [[int(r) for r in row[0:2]] for row in reader]

    print "Reading and parsing the data into memory..."
    if isDirected:
        return parse_directed(data)
    else:
        return parse_undirected(data)

def parse_directed(data):
    DG = nx.DiGraph()

    for row in data:

        node_a = row[0]
        node_b = row[1]

        DG.add_edge(node_a, node_b)
        DG.add_path([node_a, node_b])

    return DG

def digits(val):
    return int(re.sub("\D", "", val))
