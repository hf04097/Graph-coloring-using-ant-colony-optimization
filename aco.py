import matplotlib.colors as mcolors
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice
from graph import Graph


class Ant:
    def __init__(self, problem, pheromones, pheromonesInitVal):
        self.problem = problem
        self.problemInstance = self.problem.initAnt()
        self.pheromones = pheromones
        self.pheromonesInitVal = pheromonesInitVal

    def makeTour(self, alpha, gamma, iterations):
        self.edgesVisited = []
        currentNode, done = self.problemInstance.currentState()
        while not done:
            neighbors = self.problemInstance.getNeighbours()
            probs = []
            for n in neighbors:
                if (currentNode, n) not in self.pheromones:
                    self.pheromones[(currentNode, n)] = self.pheromonesInitVal * gamma ** iterations
                probs.append(self.pheromones[(currentNode, n)])
            summ = sum(map(lambda x: x ** alpha, probs))
            actualProbs = [x**alpha / summ for x in probs]
            nextNeigh = neighbors[choice(range(len(neighbors)), p=actualProbs)]
            self.edgesVisited.append((currentNode, nextNeigh))
            currentNode, done = self.problemInstance.colorNextVertex(nextNeigh)
        
    def resetPosition(self):
        self.problemInstance = self.problem.initAnt()

    def updatePheromones(self, scale):
        reward = self.problemInstance.getReward()
        for i in self.edgesVisited:
            self.pheromones[i] += reward * scale



class ACO:
    def __init__(self, problem, alpha = 1.2, beta = 0.8, gamma = 1):
        self.problem = problem
        self.pheromones = dict()
        self.pheromonesInitVal = 1
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def evaporate(self):
        for i in self.pheromones:
            self.pheromones[i] *= self.gamma
        
    def performACO(self, numAnts, iterations):
        ants = [Ant(self.problem, self.pheromones, self.pheromonesInitVal) for i in range(numAnts)]
        rewards = []
        for i in range(iterations):
            thisIterRewards = []
            for a in ants:
                a.resetPosition()
                a.makeTour(self.alpha, self.gamma, iterations)
                thisIterRewards.append(a.problemInstance.getPerformance())
            self.evaporate()
            for a in ants:
                a.updatePheromones(1)
            rewards.append(thisIterRewards)
        # print(self.pheromones)
        rewards = np.array(rewards)
        plt.figure()
        plt.plot(rewards.mean(axis = 1))
        plt.show()

        plt.figure()
        plt.plot(np.minimum.accumulate(rewards.min(axis = 1)))
        plt.show()

if __name__ == "__main__":
    g = Graph()
    gr, col = g.create_graph('gcol1.txt')
    g.depthFirstSearch()

    aco = ACO(g, 1.66, 0.58, 0.9)
    aco.performACO(30, 100)