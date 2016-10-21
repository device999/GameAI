import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from dijkstra import dijkstra
from A_asterisk import A_ast
import numpy as np

def main(datapath, start, stop, method):
    data = pd.read_csv(datapath,header=None,sep=' ')
    dd = data.as_matrix()

    dd =dd[::-1].transpose().copy()
    dots = [(i,j) for i in range(dd.shape[0]) for j in range(dd.shape[1]) if dd[i,j]==0]
    g = nx.Graph()
    g.add_nodes_from(dots)

    g.add_weighted_edges_from(((i, j), (i - 1, j), 1) for i,j in g.nodes() if (i -1, j) in g.nodes())
    g.add_weighted_edges_from(((i, j), (i, j - 1), 1) for i,j in g.nodes() if (i, j -1) in g.nodes())

    pos = dict( (n, n) for n in g.nodes() )
    labels = dict( ((i, j), '%s,%s'%(i,j)) for i,j in g.nodes() )
    nx.draw_networkx(g, pos=pos, labels=labels,node_size = 10, with_labels=False, node_color='w')
    if method=='d':
        results = dijkstra(g, start, stop)
    elif method =='a':
        results = A_ast(g, start, stop)
    path_edges = [el for el in zip(results[0], results[0][1:])]

    nx.draw_networkx_nodes(g, pos, nodelist=results[2], node_color= 'g', node_size = 30)
    nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='r', width=5)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    from optparse import OptionParser
    import sys
    parser = OptionParser()
    parser.add_option("-d", "--data", dest="data", default=False,
                      help="Give data option")
    parser.add_option("-s", "--start", dest="start", default=(0,0),
                      help="Give start option")
    parser.add_option("-e", "--stop", dest="stop", default=(0, 0),
                      help="Give stop option")
    parser.add_option("-m", "--method", dest="method", default='d',
                      help="Give method option")
    (options, args) = parser.parse_args()
    print(options)
    #datapath = '/home/phil/Downloads/simpleMap-4-22x34.txt'
    if options.data:
        datapath = sys.path[0]+'/' + options.data
    else:
        print('no data specified')
        raise SystemExit
    main(datapath, eval(options.start),eval(options.stop),options.method)