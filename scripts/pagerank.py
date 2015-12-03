import operator
import math, random, sys, csv
import dirs, utils, helpers

class PageRank:
    def __init__(self, graph, directed):
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85
        self.directed = directed
        self.ranks = dict()
    
    def rank(self):
        for key, node in self.graph.nodes(data=True):
            if self.directed:
                self.ranks[key] = 1/float(self.V)
            else:
                self.ranks[key] = node.get('rank')

        for _ in range(10):
            for key, node in self.graph.nodes(data=True):
                rank_sum = 0
                curr_rank = node.get('rank')
                if self.directed:
                    neighbors = self.graph.out_edges(key)
                    for n in neighbors:
                        outlinks = len(self.graph.out_edges(n[1]))
                        if outlinks > 0:
                            rank_sum += (1 / float(outlinks)) * self.ranks[n[1]]
                else: 
                    neighbors = self.graph[key]
                    for n in neighbors:
                        if self.ranks[n] is not None:
                            outlinks = len(self.graph.neighbors(n))
                            rank_sum += (1 / float(outlinks)) * self.ranks[n]
            
                # actual page rank compution
                self.ranks[key] = ((1 - float(self.d)) * (1/float(self.V))) + self.d*rank_sum

        return p

def rank(graph, node):
    #V
    nodes = graph.nodes()
    #|V|
    nodes_sz = len(nodes) 
    #I
    neighbs = graph.neighbors(node)
    #d
    rand_jmp = random.uniform(0, 1)

    ranks = []
    ranks.append( (1/nodes_sz) )
    
    for n in nodes:
        rank = (1-rand_jmp) * (1/nodes_sz) 
        trank = 0
        for nei in neighbs:
            trank += (1/len(neighbs)) * ranks[len(ranks)-1]
        rank = rank + (d * trank)
        ranks.append(rank)

def write_ranks(rks_dict):
    discovery_list, discovery_header = helpers.load_csv(dirs.dirs_dict["discoveries"]["instagram"])
    for i in range(len(discovery_list)):
        discovery_list[i]["pagerank"] = rks_dict[discovery_list[i]["user_id"]]
    discovery_header.append("pagerank")
    discovery_list.sort(key=lambda k: k["pagerank"], reverse=True)
    helpers.write_csv(dirs.dirs_dict["discoveries"]["instagram"]+"-pageranked", discovery_list, discovery_header)
    return None

if __name__ == '__main__':
    filename = dirs.dirs_dict["relationships"]["instagram"]+".csv"
    isDirected = True

    graph = utils.parse(filename, isDirected)
    p = PageRank(graph, isDirected)
    p.rank()
    
    pageranks = {k: v for k, v in p.ranks.iteritems()}
    write_ranks(pageranks)


 