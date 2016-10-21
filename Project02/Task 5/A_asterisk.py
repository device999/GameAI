from scipy.spatial import distance as _d
import numpy as np
def A_ast(g,start,stop):

    # closed ← ∅
    # fringe ← {s}
    # g[s] ← 0
    # f[s] ← g[s] + h(s, t)
    # while fringe 6= ∅
    # u ← argmin n ∈ fringe f[n]
    # if u = t break
    # closed ← closed ∪ {u}
    # fringe ← fringe \ {u}
    # for v ∈ Neib(u) \ closed
    #     newg ← g[u] + wuv
    #     if v ∈/ fringe ∨ g[v] > newg
    #         g[v] ← newg
    #         f[v] ← g[v] + h(v, t)
    #         p[v] ← u
    #         if v ∈/ fringe
    #             fringe ← fringe ∪ {v}

    nodes = g.nodes()
    G = g.edge
    dist = {node: np.inf for node in nodes}
    closed = []
    current = start
    currentDistance = 0
    dist[current] = currentDistance
    path = {}
    finished  = False
    while not finished:
        for neighbour, distance in G[current].items():
            if (dist[neighbour] > currentDistance + distance['weight']) and neighbour not in closed:
                dist[neighbour] = currentDistance + distance['weight']
                path[neighbour] = current
            if neighbour == stop:
                finished = True
        closed.append(current)
        print(current)
        candidates = [node for node in dist.items() if node[0] not in closed]

        if not candidates:
            finished = True
        else:
            current, currentDistance = sorted(candidates, key=lambda x: x[1] + _d.euclidean(x[0],stop), reverse=False)[0]

    def _tracer(start, k, path, route):
        route.insert(0, k)
        while route[0] != start:
            _tracer(start, path[k], path, route)
        return route

    route = _tracer(start, stop, path, [])

    return route, dist[stop], closed
