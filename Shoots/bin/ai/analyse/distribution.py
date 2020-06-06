import matplotlib.pyplot as plt
import math

from Shoots.bin.ai.train_cfr import Training,Node

training = Training(0)
training.load("cur_train.params")

def count_column(nodeMap, bitmap_label=None, history_label=None):
    data = {}
    for k in nodeMap:
        if bitmap_label and k[bitmap_label[0]:bitmap_label[0]+1] != bitmap_label[1]:
            continue
        if history_label and history_label not in k:
            continue
        strategy = nodeMap[k].getStrategy(1)
        action = strategy.index(max(strategy))
        data[action] = data.get(action, 0) + 1
    return data

def count_all(nodeMap):

    bitmap_divide = 5

    data = {}
    for k in nodeMap:
        bitmap = k[:bitmap_divide]
        history = k[bitmap_divide:]
        if len(bitmap) > 0:
            for i in range(len(bitmap)):
                if i not in data:
                    data[i] = count_column(nodeMap, [i, "1"])
        if len(history) > 0:
            for i in range(0, len(history), 2):
                action = history[i:i+2]
                if action not in data:
                    data[action] = count_column(nodeMap, history_label=action)
    return data

# data = count_column(training.nodeMap, [0, "1"])
data = count_all(training.nodeMap)
print(data)

def draw_one(plt, data, training):
    numbers = [0] * training.num_actions
    labels = list(range(training.num_actions))
    for k in data:
        numbers[k] = data[k]

    plt.bar(labels, numbers, tick_label=labels)

colums = math.ceil(math.sqrt(len(data)))

for i, k in enumerate(data):
    sp = plt.subplot(colums, colums, i+1)
    sp.title.set_text(k)
    draw_one(sp, data[k], training)

plt.show()