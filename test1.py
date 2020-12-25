import time
import random
from neuralnet import NeuralNet

LAYERS = 4
WIDTH = 7

NN = NeuralNet(LAYERS, WIDTH)

NN.visual_init()

while(True):
    NN.read_inputs([random.random() for i in range(WIDTH)])
    NN.compute()
    time.sleep(1)