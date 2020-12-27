import time
import random
from neuralnet import NeuralNet

LAYERS = 4
WIDTHS = (3, 7, 4, 2)

NN = NeuralNet(LAYERS, WIDTHS)

NN.visual_init()

while(True):
    NN.read_inputs([random.random() for i in range(WIDTHS[0])])
    NN.compute()
    time.sleep(1)
