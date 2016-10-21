import numpy as np
def dijkstra(g, start, stop):
    nodes = g.nodes()
    G = g.edge
    dist = {node: np.inf for node in nodes}
    closed = []

    current = start
    currentDistance = 0
    dist[current] = currentDistance
    #
    # while fringe 6= ∅
    #   u ← argmin d[n] n ∈ fringe
    #   closed ← closed ∪ {u}
    #   fringe ← fringe \ {u}
    #   for v ∈ Neib(u) \ closed
    #       if d[v] > d[u] + wuv
    #           d[v] ← d[u] + wuv
    #           p[v] ← u
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
        candidates = [node for node in dist.items() if node[0] not in closed]
        if not candidates:
            finished = True
        current, currentDistance = sorted(candidates, key=lambda x: x[1], reverse=False)[0]

    def _tracer(start, k, path, route):
        route.insert(0, k)
        while route[0] != start:
            _tracer(start, path[k], path, route)
        return route

    route = _tracer(start,stop,path,[])

    return route, dist[stop], closed
