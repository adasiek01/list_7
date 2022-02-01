import itertools
import graphviz

picture = graphviz.Digraph(filename='graph', comment='The graph')
picture2 = graphviz.Digraph(filename='graph_2', comment='The graph_2')


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class PriorityQueue:
    def __init__(self):
        self.heapArray = [(0, 0)]
        self.currentSize = 0

    def buildHeap(self, alist):
        self.currentSize = len(alist)
        self.heapArray = [(0, 0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2            
        while (i > 0):
            self.percDown(i)
            i = i - 1
                        
    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc
                
    def minChild(self, i):
        if i*2 > self.currentSize:
            return -1
        else:
            if i*2 + 1 > self.currentSize:
                return i*2
            else:
                if self.heapArray[i*2][0] < self.heapArray[i*2+1][0]:
                    return i*2
                else:
                    return i*2+1

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i//2][0]:
               tmp = self.heapArray[i//2]
               self.heapArray[i//2] = self.heapArray[i]
               self.heapArray[i] = tmp
            i = i//2
 
    def add(self, k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval
        
    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self, val, amt):
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt, self.heapArray[myKey][1])
            self.percUp(myKey)
            
    def __contains__(self, vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False


class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'
        self.dist = float("inf")
        self.pred = None
        self.disc = 0
        self.fin = 0

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color
        
    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime
        
    def setFinish(self, ftime):
        self.fin = ftime
        
    def getFinish(self):
        return self.fin
        
    def getDiscovery(self):
        return self.disc
        
    def getPred(self):
        return self.pred
        
    def getDistance(self):
        return self.dist
        
    def getColor(self):
        return self.color

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

    def addEdge(self, f, t, cost=1):
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

    def display(self):
        picture.view()

    def __contains__(self, n):
        return n in self.vertList

    def __iter__(self):
        return iter(self.vertList.values())

    def bfs(g, start):
        start.setDistance(0)
        start.setPred(None)
        vertQueue = Queue()
        vertQueue.enqueue(start)
        while vertQueue.size() > 0:
            currentVert = vertQueue.dequeue()
            for nbr in currentVert.getConnections():
                if nbr.getColor() == 'white':
                    nbr.setColor('gray')
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)
                    vertQueue.enqueue(nbr)
            currentVert.setColor('black')


class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self.time = 0

    def dfs(self):
        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex)

    def dfsvisit(self, startVertex):
        startVertex.setColor('gray')
        self.time += 1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
        startVertex.setColor('black')
        self.time += 1
        startVertex.setFinish(self.time)

    def sort(self, key):
        """
        Firstly function visits the nodes. Creates list of tuples (key, vertex), then graph and prints the list.
        :param: key - key of the node we start searching
        """
        self.dfsvisit(self.getVertex(key))
        list_1 = sorted(self.vertList.items(), key=lambda x: (x[1]).fin, reverse=True)
        i = 0
        
        while i+1 <= len(list_1)-1:
            picture2.edge(str(list_1[i][0]), str(list_1[i+1][0]))
            i += 1
        
        picture2.view()
        print(list_1)

    def water(self, first_canister=3, second_canister=4, result=2):
        """
        Function creates list of tuples (size=2). First coordinate = amount of water in first canister,
        second coordinate = amount of water in second canister. Checks the options and creates edges and the graph.
        :param: first_canister - first canister
        :param: second_canister - second canister
         :param: result - the number of liters obtained
        """
        first_possibilities = [item for item in range(0, first_canister +1)]
        second_possibilities = [item for item in range(0, second_canister +1)]

        all_tuples = list(itertools.product(first_possibilities, second_possibilities))

        print(all_tuples)
        for tuple in all_tuples:
            x_1 = (first_canister, tuple[1])                   # fill up 1
            x_2 = (tuple[0], second_canister)                   # fill up 2
            x_3 = (0, tuple[1])                   # empty 1
            x_4 = (tuple[0], 0)                   # empty 2
            if tuple[0]+tuple[1] < first_canister:
                x = (tuple[0]+tuple[1], 0)             # pour over from 2 to 1
                if x in all_tuples and x != tuple:
                    self.addEdge(tuple, x)  
            if tuple[0]+tuple[1] < second_canister:
                x = (0, tuple[0]+tuple[1])             # pour over from 1 to 2
                if x in all_tuples and x != tuple:
                    self.addEdge(tuple, x)   
            if tuple[0]+tuple[1] >= first_canister:
                y = (first_canister, tuple[1]-first_canister+tuple[0])             # pour over from 2 to 1
                if y in all_tuples and y != tuple:
                    self.addEdge(tuple, y)         
            if tuple[0]+tuple[1] >= second_canister:
                z = (tuple[0]-second_canister+tuple[1], second_canister)             # pour over from 1 to 2
                if z in all_tuples and z != tuple:
                    self.addEdge(tuple, z)        
            
            if x_1 in all_tuples and x_1 != tuple:
                self.addEdge(tuple, x_1)
            if x_2 in all_tuples and x_2 != tuple:
                self.addEdge(tuple, x_2)
            if x_3 in all_tuples and x_3 != tuple:
                self.addEdge(tuple, x_3)
            if x_4 in all_tuples and x_4 != tuple:
                self.addEdge(tuple, x_4)
            
        self.display()
        dijkstra(self, self.getVertex((0,0)),result)


def dijkstra(aGraph, start, result):
    """
    Function builds heap from the list of tuples. Goes through each node in graph
    :param: aGraph - graph where we search the shortest path
    :param: start - node we start counting paths
    :param" result - the number of liters obtained
    """
    pq = PriorityQueue()
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(), v) for v in aGraph])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
            if newDist < nextVert.getDistance():
                nextVert.setDistance(newDist)
                nextVert.setPred(currentVert)
                pq.decreaseKey(nextVert, newDist)

    for apex in [aGraph.getVertex((0,result)), aGraph.getVertex((result, 0))]:
        print("Shortest path from " + str(start.id) + " to " + str(apex.id) + ", distance: " + str(apex.dist))
        
        list_1 = []
    
        while apex != start:
            print(type(apex))
            print(apex.id)
            list_1.append(apex.id)
            if apex.getPred:
                apex = apex.getPred()

        list_1.append(start.id)
        list_1.reverse()
        print(list_1)


if __name__ == '__main__':
    d = DFSGraph()
    d.water(5, 6, 3)
