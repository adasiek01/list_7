import graphviz

picture = graphviz.Digraph(filename='graph', comment='The graph')


class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
    
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight
        
    def getPred(self):
        return self.pred

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.edgeList = []
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        picture.node(name=str(key), label=str(key))
        return newVertex

    def addVertices(self, list_1):
        """
        Function creates nodes of given keys.
        :param: list_1 - list of keys for new objects
        """
        for key in list_1:
            self.addVertex(key)

    def getVertex(self, key):
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None
    
    def getVertices(self):
        return self.vertList.keys()

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)
        self.edgeList.append((f,t))
        picture.edge(str(f), str(t), str(cost))

    def addEdges(self, list_1):
        """
        Function creates edge of graph for every tuple
        :param: list_1 - list of tuple that has size=3 (start of the edge, end, weight)
        """
        for edge in list_1:
            self.addEdge(edge[0], edge[1], edge[2])

    def getEdges(self):
        """
        Function returns every nodes of graph i 2-element tuple
        """
        return self.edgeList

    def visualize(self):
        picture.view()

    def __contains__(self, n):
        return n in self.vertList

    def __iter__(self):
        return iter(self.vertList.values())


    def miss_can(self, initial_miss, initial_can):
        """
        Function creates list of tuples (size=3) that define situation at beginning. First coordinate is a number of
        missionaries, second cannibals, third is the coast (0 or 1). Then checks task conditions and possible options
        to move. Then creates nodes which are the keys do the tuple and creates edge and The graph.
        :param: initial_miss - missionaries
        :param: inital_can - cannibals
        """
        possible_tuples = []
        for m in range(1, initial_miss + 1):
            for c in range(0, m + 1):
                for b in range(0, 2):
                    tupl = (m, c, b)
                    possible_tuples.append(tupl)
        m = 0
        for c in range(0, initial_can + 1):
            for b in range(0, 2):
                tupl = (m, c, b)
                possible_tuples.append(tupl)

        for tuples in possible_tuples:
            if tuples[0] != 0 and tuples[0] != 3:
                if not (initial_miss - tuples[0] >= initial_can - tuples[1] and tuples[0] >= tuples[1]):
                    possible_tuples.remove(tuples)

        moves = [(0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 1), (2, 0, 1)]

        for tuple in possible_tuples:
            for move in moves:
                if tuple[2] == 1:
                    wanted = (tuple[0] - move[0], tuple[1] - move[1], tuple[2] - move[2])
                    if wanted in possible_tuples:
                        self.addEdge(tuple, wanted, move)

                if tuple[2] == 0:
                    wanted = (tuple[0] + move[0], tuple[1] + move[1], tuple[2] + move[2])
                    if wanted in possible_tuples:
                        self.addEdge(tuple, wanted, move)

        a.visualize()


if __name__ == '__main__':
    a = Graph()
    a.miss_can(3, 3)
