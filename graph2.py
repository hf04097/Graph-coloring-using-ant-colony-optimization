import matplotlib.colors as mcolors
import networkx as nx
import matplotlib.pyplot as plt
from random import choice



class ColorState:
    def __init__(self, graph):
        self.graph = graph
        self.startVertex = 1
        self.visited = [self.startVertex]
        self.colors = [self.graph.colors[0]]
        self.done = len(self.visited) == len(self.graph.V)

    def getNeighbours(self):
        return list(self.graph.V - set(self.visited))

    def colorNextVertex(self, vertex):
        neighborColors = {self.colors[self.visited.index(i)] for i in self.graph.AdjList[vertex] if i in self.visited}
        self.visited.append(vertex)
        for i in self.graph.colors:
            if i not in neighborColors:
                self.colors.append(i)
                break
        self.done = len(self.visited) == len(self.graph.V)
        return vertex, self.done

    def currentState(self):
        return self.visited[-1], self.done

    def rewardMetric1(self):
        rawRew = len(set(self.colors))
        if rawRew > 30:
            return 0
        return (30 - rawRew)

    def rewardMetric2(self):
        rawRew = len(set(self.colors))
        if rawRew < 20:
          return 50
        return 20 / (rawRew)

    def getReward(self):
        if not self.done:
            raise Exception("Reward called before done")
        return self.rewardMetric2()

    def getPerformance(self):
        if not self.done:
            raise Exception("Reward called before done")
        return len(set(self.colors))


class Graph:
    def __init__(self):
        self.G = []
        self.V = set()
        self.colors = []
        self.number_of_nodes = 0
        self.number_of_edges = 0

    def create_graph(self, filename):
        f = open(filename, 'r')
        line_1 = True
        for i in f.readlines():
            node = i.split(" ")
            if line_1:
                self.number_of_nodes = int(node[2])
                self.number_of_edges = int(node[3])
                line_1 = False
            else:
                self.G.append((int(node[1]), int(node[2])))

        for name, code in mcolors.CSS4_COLORS.items():
            self.colors.append(code)  # 148 size

        self.V = set(j for i in self.G for j in i)
        self.colors = list(set(self.colors))[:self.number_of_nodes]  # 138 size
        self.makeAdjList()

        return self.G, self.colors

    def is_coloring(self):
        for i in self.G:
            if self.colors[i[0] - 1] == self.colors[i[1] - 1]:
                return False
        return True

    def draw_graph(self):
        nx_graph = nx.Graph()
        for i in self.G:
            nx_graph.add_edge(i[0],i[1])
        nx.draw(nx_graph, node_color = self.colors)
        plt.draw()
        plt.show()

    def makeAdjList(self):
        self.AdjList = {v:set() for v in self.V}
        for i in self.G:
            self.AdjList[i[0]].add(i[1])
            self.AdjList[i[1]].add(i[0])
        return self.AdjList

    def initAnt(self):
        return ColorState(self)

    def depthFirstSearch(self):
        pass


if __name__ == "__main__":
    g = Graph()
    gr, col = g.create_graph('gcol1.txt')
    g.depthFirstSearch()

    cs = ColorState(g)
    currentState, done = cs.currentState()
    while not done:
        verCol = choice(cs.getNeighbours())
        currentState, done = cs.colorNextVertex(verCol)
    g.colors = cs.colors
    print(len(set(g.colors)))

    g.draw_graph()
