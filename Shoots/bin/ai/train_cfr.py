from typing import Dict
import copy
import random
import pickle
import time

from Shoots.bin.info import Info
from Shoots.bin.shoots import Shoots
from Shoots.bin.ai.shooter import CFRShooter
from Shoots.bin.ai.shooter import RandomAIShooter

class Node:
    def __init__(self, num_actions, infoSet):
        self.infoSet = infoSet
        self.num_actions = num_actions
        self.regretSum = [0] * self.num_actions # positive mean hope to do, negative mean hope not to do
        self.strategy = [0] * self.num_actions # normalized regretSum, negative regret will be 0, represent the possibility of winning
        self.strategySum =  [0] * self.num_actions # with realizationWeight's strategy

    def getStrategy(self, realizationWeight) -> list:
        normalizingSum = 0
        for a, v in enumerate(self.regretSum):
            self.strategy[a] = v if v > 0 else 0
            normalizingSum += self.strategy[a]
        for a in range(self.num_actions):
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1 / self.num_actions
            self.strategySum[a] += realizationWeight * self.strategy[a]
        return self.strategy

    def getAverageStrategy(self) -> float:
        avgStrategy = [0] * self.num_actions
        normalizingSum = sum(self.strategySum)
        for a in range(self.num_actions):
            if normalizingSum > 0:
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1 / self.num_actions
    
    def update(self, utils:list):
        self.getStrategy(1)
        nodeUtil = sum([self.strategy[a] * utils[a] for a in range(self.num_actions)])
        for a in range(self.num_actions):
            self.regretSum[a] += utils[a] - nodeUtil
        return nodeUtil

    def __repr__(self):
        return str(self.getStrategy(1))

class Training:
    """
    http://modelai.gettysburg.edu/2013/cfr/cfr.pdf 3.4 Kuhn Poker Page: 11
    """

    class Trainer:
        def __init__(self, max_recursion_depth, num_actions, nodeMap:Dict[str, Node]):
                self.max_recursion_depth = max_recursion_depth
                self.current_recursion_depth = 0
                self.loading_progress = 0
                self.nodeMap = nodeMap
                self.num_actions = num_actions
                self.history_window = 1

        def print_loading(self):
            self.loading_progress += 1
            m = {
                0:"-",
                1:"\\",
                2:"|",
                3:"/"
            }
            if self.loading_progress >= 4:
                self.loading_progress = 0
            print("training... {}".format(m[self.loading_progress],), end="\b\r")

        def cfr(self, server:Shoots, history:str, player_id:int) -> float:
            self.print_loading()
            if self.max_recursion_depth <= self.current_recursion_depth:
                # print("reached max recursion depth")
                return 0
            self.current_recursion_depth += 1
            server.update_model()
            
            if [i.dead for i in server.players].count(False) == 1:
                actions = len(history) / 2

                win = 1 if not server.players[player_id].dead else -1

                # winner with less actions gets higher score, 
                # loser with more actions (longer survival time) gets higher score
                score = win * ((1 / actions) if actions > 0 else 0)

                self.current_recursion_depth -= 1
                return score

            util = [0] * self.num_actions # score of every action

            for a in range(self.num_actions):
                nextHistory = history + server.players[player_id].mapAction(a)

                newServer = copy.deepcopy(server)

                newServer.process_input(newServer.players[player_id], a)

                util[a] = self.cfr(newServer, nextHistory, player_id)

            infoSet = server.players[player_id].genInfoSet(self.history_window)
            node = self.__getNode(infoSet)
            nodeUtil = node.update(util)

            self.current_recursion_depth -= 1
            return nodeUtil
        
        def __getNode(self, infoSet):
            if not infoSet in self.nodeMap:
                self.nodeMap[infoSet] = Node(self.num_actions, infoSet)
            return self.nodeMap[infoSet]

    def __init__(self, max_recursion_depth):
        self.max_recursion_depth = max_recursion_depth
        self.nodeMap:Dict[str, Node] = {}
        self.num_actions = 9
        self.history_window = 1

    def train(self, iterations):
        
        print(f"total epoch: {iterations}, {self.num_actions ** self.max_recursion_depth} route per epoch")
        for i in range(iterations):
            print("epoch: {}, start at: {}\033[K".format(i+1, time.asctime()))
            server = Shoots()
            server.players = [] # clear all players

            server.map.size = 5
            server.map.map = [
                [server.map.ROAD] * 5
            ] * 5

            for i in server.map.get_view():
                for j in i:
                    print(j, end='')
                print()

            p1 = CFRShooter(server.map)
            p2 = CFRShooter(server.map)
            print(f"initial position: p1{p1.position}, p2{p2.position}")
            server.players.append(p1)
            server.players.append(p2)

            trainer = Training.Trainer(self.max_recursion_depth, self.num_actions, self.nodeMap)
            trainer.cfr(server, '', 0)

            self.save("cur_train.params")

    def save(self, filename):
        with open(filename, "wb") as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, "rb") as input:
            t = pickle.load(input)
            self.max_recursion_depth = t.max_recursion_depth
            self.nodeMap:Dict[str, Node] = t.nodeMap
            self.num_actions = t.num_actions

    def print_nodeMap(self):
        print("{")
        for k in sorted(self.nodeMap):
            print("\t", k, "\n\t", self.nodeMap[k], ",")
        print("}")

def show_trained():
    trainer = Training(0)
    trainer.load("cur_train.params")
    trainer.print_nodeMap()

if __name__ == "__main__":
    import sys, time
    print(sys.argv)
    if len(sys.argv) > 1:
        show_trained()
        exit(0)
    
    print("load trained params", "cur_train.params")
    trainer = Training(0)
    try:
        trainer.load("cur_train.params")
    except FileNotFoundError:
        print("not found", "cur_train.params", "start from fresh")

    # resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    max_recursion_depth = 6
    sys.setrecursionlimit(max_recursion_depth*10) # some built-in functions need recursion
    print("max_recursion_depth=", max_recursion_depth)

    trainer.max_recursion_depth = max_recursion_depth

    trainer.train(30)
    trainer.print_nodeMap()