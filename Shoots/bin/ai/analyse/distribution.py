import matplotlib.pyplot as plt

from Shoots.bin.ai.train_cfr import Training,Node

training = Training(0)
training.load("./Shoots/bin/ai/analyse/100-epoch-still.params")
training.print_nodeMap()

def count_column(nodeMap, label_column_num):
    data = {}
    for k in nodeMap:
        if k[label_column_num:label_column_num+1] != "1":
            continue
        strategy = nodeMap[k].getStrategy(1)
        action = strategy.index(max(strategy))
        data[action] = data.get(action, 0) + 1
    return data
data = count_column(training.nodeMap, 0)

numbers = [0] * training.num_actions
labels = list(range(training.num_actions))
for k in data:
    numbers[k] = data[k]


plt.bar(labels, numbers, tick_label=labels)

plt.show()