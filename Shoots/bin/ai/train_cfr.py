from typing import Dict
import copy
import random
import pickle

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

    def __repr__(self):
        return str(self.getStrategy(1))

class Training:
    """
    http://modelai.gettysburg.edu/2013/cfr/cfr.pdf 3.4 Kuhn Poker Page: 11
    """
    def __init__(self, max_recursion_depth):
        self.max_recursion_depth = max_recursion_depth
        self.current_recursion_depth = 0
        self.random = random.Random()
        self.nodeMap:Dict[str, Node] = {}
        self.num_actions = 9
        self.loading_progress = 0

    def train(self, iterations):
        
        win_count = 0
        print(f"total epoch: {iterations}, {self.num_actions ** self.max_recursion_depth} route per epoch")
        for i in range(iterations):
            print("epoch: {}\033[K".format(i+1,))
            server = Shoots()
            server.players = [] # clear all players

            p1 = CFRShooter(server.map)
            p2 = CFRShooter(server.map)
            server.players.append(p1)
            server.players.append(p2)

            self.save("cur_train.params")

            win_count += 1 if self.__cfr(server, '', p1, p2) else 0

        print("win rate:", win_count / iterations)

    def save(self, filename):
        with open(filename, "wb") as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, "rb") as input:
            t:Training = pickle.load(input)
            self.max_recursion_depth = t.max_recursion_depth
            self.current_recursion_depth = t.current_recursion_depth
            self.random = t.random
            self.nodeMap:Dict[str, Node] = t.nodeMap
            self.num_actions = t.num_actions
            self.loading_progress = t.loading_progress

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


    def __cfr(self, server:Shoots, history:str, p1:CFRShooter, p2:RandomAIShooter) -> float:
        self.print_loading()
        if self.max_recursion_depth <= self.current_recursion_depth:
            # print("reached max recursion depth")
            return -1
        self.current_recursion_depth += 1
        server.update_model()

        if [i.dead for i in server.players].count(False) == 1:
            actions = len(history)

            win = 1 if not p1.dead else -1

            # winner with less actions gets higher score, 
            # loser with more actions (longer survival time) gets higher score
            score = win * ((1 / actions) if actions > 0 else 0)

            self.current_recursion_depth -= 1
            return score

        infoSet = self.__genInfoSet(p1)
        
        if not infoSet in self.nodeMap:
            self.nodeMap[infoSet] = Node(self.num_actions, infoSet)
        node = self.nodeMap[infoSet]
        strategy = node.getStrategy(1)
        util = [0] * self.num_actions # score of every action
        nodeUtil = 0 # sum of score

        for a in range(self.num_actions):
            nextHistory = history + self.__mapAction(a)

            newServer = copy.deepcopy(server)
            newServer.process_input(newServer.players[0], a)
            p2.action()
            util[a] = self.__cfr(newServer, nextHistory, newServer.players[0], newServer.players[1])
            nodeUtil += strategy[a] * util[a]

        for a in range(self.num_actions):
            regret = util[a] - nodeUtil
            node.regretSum[a] += regret

        self.current_recursion_depth -= 1
        return nodeUtil
        
    def __genInfoSet(self, shooter:CFRShooter) -> str:
        """
        build infoSet
        path avaliable: up down left right
        facing enemy: 

        """
        infoSet = ""
        map = shooter.map
        position = shooter.position
    
        np = (position[0]-1, position[1])
        infoSet += "1" if map.is_road(np) else "0"

        np = (position[0]+1, position[1])
        infoSet += "1" if map.is_road(np) else "0"

        
        np = (position[0], position[1]-1)
        infoSet += "1" if map.is_road(np) else "0"

        
        np = (position[0], position[1]+1)
        infoSet += "1" if map.is_road(np) else "0"

        infoSet += "1" if len(shooter.info.shooter) > 0 else "0"
        return infoSet

    def __mapAction(self, action):
        return {
            Info.OP_MOVE_UP:"mu",
            Info.OP_MOVE_DOWN:"md",
            Info.OP_MOVE_LEFT:"ml",
            Info.OP_MOVE_RIGHT:"mr",
            Info.FACE_UP:"fu",
            Info.FACE_DONW:"fd",
            Info.FACE_LEFT:"fl",
            Info.FACE_RIGHT:"fr",
            Info.OP_SHOOT:"st"
        }[action]
    
    def print_nodeMap(self):
        print("{")
        for k in self.nodeMap:
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
    max_recursion_depth = 5
    sys.setrecursionlimit(max_recursion_depth*10) # some built-in functions need recursion
    print("max_recursion_depth=", max_recursion_depth)

    trainer.max_recursion_depth = max_recursion_depth

    trainer.train(100)
    for k in trainer.nodeMap:
        print(k, trainer.nodeMap[k])