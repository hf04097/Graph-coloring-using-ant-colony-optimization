import matplotlib.colors as mcolors
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.G = []
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

        self.colors = list(set(self.colors))[:self.number_of_nodes]  # 138 size

        return self.G, self.colors

    def is_coloring(self):
        for i in self.G:
            if self.colors[i[0]] == self.colors[i[1]]:
                return False
        return True

    def draw_graph(self):
        nx_graph = nx.Graph()
        for i in self.G:
            nx_graph.add_edge(i[0],i[1])
        nx.draw(nx_graph, node_color = self.colors)
        plt.draw()
        plt.show()




g = Graph()
gr, col = g.create_graph('gcol1.txt')
#print(g.is_coloring())
g.draw_graph()
