from random import choice
from copy import deepcopy
import sys

class Karger_Mincut:
    def __init__(self,data_path):
        self.data_path = data_path

    def get_graph(self):
        # function to get graph dictionary
        graph = {}
        with open(self.data_path) as f:
            for line in f:
                v1, v2 = map(str, line.strip().split())
                if v1 not in graph:
                    graph[v1] = []
                if v2 not in graph:
                    graph[v2] = []
                graph[v1].append(v2)
                graph[v2].append(v1)
        return graph
    
    def contract(self,graph):
        # function chooses random edge and absorb the nodes into 1 
        u = choice(list(graph.keys()))
        v = choice(graph[u])
        new_key = u+"-"+v # create new key 
        graph[new_key] = graph[u] + graph[v] # absorb u,v into u + '_' + v 
        del graph[u] # delete chosen edges node
        del graph[v] # delete chosen edges node
        for key in graph.keys():
            copy = graph[key][:]
            if new_key == key:
                for item in copy:
                    if item == u or item == v:
                        graph[key].remove(item)
            else:
                for item in copy:
                    if item == u or item == v:
                        graph[key].remove(item)
                        graph[key].append(new_key)
        return graph
    
    def min_cut(self):
        # excutes the contract function untill there is only 2 edges
        # get a copy of original graph
        graph = self.get_graph()
        copy =  deepcopy(graph)
        while len(copy) > 2:
            community = self.contract(copy)
        # return the required 
        mincut = len(list(community.values())[0])
        node_id = []
        for i,key in enumerate(list(community.keys())):
            if '-' in key:
                node_list = key.split('-')
                for j in node_list:
                    node_id.append([j,i+1])
            else:
                node_id.append([key,i+1])
        return mincut,node_id
    
if __name__ == "__main__":
    data_path = sys.argv[1] # get the data path 
    # create class instance
    krager_mincut = Karger_Mincut(data_path=data_path)
    # call the mincut function of the class instance to get the mincut and node_id list 
    mincut,node_id = krager_mincut.min_cut()
    # print the mincut and community nodes
    print('mincut:',mincut)
    for n in node_id:
     print(n[0], ' '.join(map(str, n[1:])))
