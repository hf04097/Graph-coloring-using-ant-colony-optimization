import matplotlib.colors as mcolors
import networkx as nx
import matplotlib.pyplot as plt
from random import choice



class ColorState:
    def __init__(self, graph):
        self.graph = graph
        self.colors = graph.colors[:2]
        self.distinctColors = set(self.colors)
        self.done = (len(self.colors) == len(self.graph.V))

    def getNeighbours(self):
        nextVert = self.graph.V2[len(self.colors)]
        colorPossibilities = []
        neighbourColors = {self.colors[i-1] for i in self.graph.AdjList[nextVert] if i-1 < len(self.colors)}
        for color in self.distinctColors:
            if color not in neighbourColors:
                colorPossibilities.append((nextVert, color))
        colorPossibilities.append((nextVert, self.graph.colors[len(self.distinctColors)]))
        return colorPossibilities

    def colorNextVertex(self, vertexColPair):
        self.colors.append(vertexColPair[1])
        self.distinctColors.add(vertexColPair[1])
        self.done = (len(self.colors) == len(self.graph.V))
        return self.currentState()

    def currentState(self):
        return (self.graph.V2[len(self.colors) - 1], self.colors[-1]), self.done

    def rewardMetric1(self):
        rawRew = len(self.distinctColors)
        if rawRew > 26:
            return 0
        return (26 - rawRew)

    def rewardMetric2(self):
        rawRew = len(self.distinctColors)
        return 10 / (rawRew)

    def getReward(self):
        if not self.done:
            raise Exception("Reward called before done")
        return self.rewardMetric2()

    def getPerformance(self):
        if not self.done:
            raise Exception("Reward called before done")
        return len(self.distinctColors)


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

    def depthFirstSearch(self):
        startVert = self.V.pop()
        self.V.add(startVert)

        stack = [startVert]
        visited = set()

        while stack and len(stack) < self.number_of_nodes:
            ele = stack[-1]
            flag = False

            for neighbor in self.AdjList[ele]:
                if neighbor not in stack and (ele, neighbor) not in visited:
                    flag = True
                    stack.append(neighbor)
                    visited.add((ele, neighbor))

            if not flag:
                stack.pop()
        
        if stack:
            print("Found hamiltonian path")
            self.V2 = stack
        else:
            print("Proceeding with random order of vertices")
            self.V2 = list(self.V)
        return self.V2

    def initAnt(self):
        return ColorState(self)

    def getNeighbours(self, colorState):
        return colorState.getNeighbours()

    def colorNextVertex(self, colorState, vertexColPair):
        return colorState.colorNextVertex(vertexColPair)

    def currentState(self, colorState):
        return colorState.currentState()


if __name__ == "__main__":
    g = Graph()
    gr, col = g.create_graph('gcol2.txt')
    g.depthFirstSearch()

    cs = ColorState(g)
    currentState, done = cs.currentState()
    while not done:
        verCol = choice(cs.getNeighbours())
        currentState, done = cs.colorNextVertex(verCol)
    g.colors = cs.colors
    print(len(set(g.colors)))

    g.draw_graph()
