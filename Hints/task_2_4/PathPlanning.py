
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math as mt

def read_File():
      f = open ( 'simpleMap-3.txt' , 'r')
      v = [ map(int,line.split(' ')) for line in f ]
      make_Graph(v)


def make_Graph(v):
    # defining start and goal nodes
    start_node = (1,1)
    end_node =(30,14)

    v = np.array(v, dtype=int)
    #get number of rows and columns
    row_len = v.shape[0]
    column_len = v.shape[1]
    # change the order of rows because in our graph the (0,0) is the left down corner
    new_order=range(row_len)[::-1]
    v1=v[new_order,:]
    #connect each node to the neighbours
    G = nx.grid_2d_graph(column_len,row_len)
    # draw the original graph
    pos = dict(zip(G,G))
    nx.draw(G,pos,node_size=50,with_labels=False)
    plt.show()

    connected_nodes=[]

     #G is a dic. of nodes connections
    for m in G:
        i=m[0]
        j=m[1]
        #find edges which equals to 1
        if v1[j][i]==1 :
           connected_nodes.append(m)
    # remove that 1 nodes from our graph
    G.remove_nodes_from(connected_nodes)

    #call functions
    dijkstra(G,start_node,end_node)

    A_star(G,start_node,end_node)

def euclidean_dis(node,end):
    result = 0
    result = mt.sqrt((node[0]-end[0])**2 +(node[1]-end[1])**2)
    result = round(result,7)
    return result

def reconstruct_path(came_from, current_node, start):
    reverse_path=[]
    position = came_from[current_node]
    reverse_path.append(current_node)
    while position != start:
         reverse_path.append(position)
         position = came_from[position]
    print 'reverse path = ', reverse_path
    return reverse_path


def A_star(G, start, end):

    openset = [start]
    closeset = []
    node = start
    g_score = {node:0}
    f_score = {}
    came_from = {}
    neighbor_nodes = {}
    g_score[node]=0
    neighbor_nodes = G[node]
    cal = 0
    f_score[start] = g_score[start] + euclidean_dis(start, end)



    # choose the smallest number
    counter =0
    while openset :
        counter +=1
        current=min(openset, key = lambda node: f_score[node])
        if current == end:
            short_path = reconstruct_path(came_from, end,start)
            print 'Length of A* algorithm = '+ str(len(short_path))
            break

        #openset.remove(current) :: I do not know why remove method here not working fine
        openset = [x for x in openset if x != current]
        if current not in closeset:
            closeset.append(current)
        neighbor_nodes = G[current]
        #f_score.pop(current)
        for neighbor in neighbor_nodes:
            if neighbor in closeset:
               pass
            else:
                # find distance between nodes (adding cost for each move)
                new_g_score = g_score[current] + (euclidean_dis(current, neighbor)/2)
            if neighbor not in closeset:
                if neighbor not in openset or new_g_score <= g_score[neighbor] :
                    #following parent of nodes
                    came_from[neighbor] = current
                    g_score[neighbor]= new_g_score
                    # we find the Euclidean current distance of our node neighbors
                    f_score[neighbor] = g_score[neighbor]+ euclidean_dis(neighbor, end)
                    if neighbor not in closeset:
                        openset.append(neighbor)
        # draw the the nodes which tasted till now , after each 10 times test
        #val_map = {start: 0.1,  end: 0.0}
        # if counter%10==0:
        #     dic_path=dict((k,0.1) for k in closeset)
        #     val_map.update(dic_path)
        #     values = [val_map.get(node,.25) for node in G.nodes()]
        #     pos = dict(zip(G,G))
        #     nx.draw(G,pos,node_size=50,node_color = values,with_labels=False)
        #  plt.show()

    #draw the path
    val_map = {start: 0.1,  end: 0.0}
    dic_path=dict((k,0.2) for k in short_path)
    val_map.update(dic_path)
    values = [val_map.get(node,.25) for node in G.nodes()]
    pos = dict(zip(G,G))
    nx.draw(G,pos,node_size=50,node_color = values,with_labels=False)
    plt.show()

def dijkstra(G,start,end):
    # use dijkstra method to find the path
    dij_path = nx.dijkstra_path(G,start ,end)
    path_len = nx.dijkstra_path_length(G,start,end)
    #print length of the path
    print "length of the Dijkstra path = "+ str(path_len)

    val_map = {start: 0.1,  end: 0.0}
    values = [val_map.get(node,.25) for node in G.nodes()]
    #draw the graph after removing nodes and start-end point of dijkstra
    pos = dict(zip(G,G))
    nx.draw(G,pos,node_size=50,node_color = values,with_labels=False)
    plt.show()

    #draw colored path of dijkstra method
    dic_path=dict((k,0.15) for k in dij_path)
    val_map.update(dic_path)
    values = [val_map.get(node,.25) for node in G.nodes()]
    pos = dict(zip(G,G))
    nx.draw(G,pos,node_size=50,node_color = values,with_labels=False)
    plt.show()


read_File()
