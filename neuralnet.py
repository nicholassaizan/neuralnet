import pygame
import threading

nodes = []

class Input:
    def __init__(self, layer_id, sub_id, weight):
        self.layer_id = layer_id
        self.sub_id = sub_id
        self.weight = weight

    def compute(self):
        return nodes[self.layer_id][self.sub_id].output * self.weight

class Function:
    def __init__(self):
        self.inputs = []
    
    def add_input(self, layer_id, sub_id, weight):
        self.inputs.append(Input(layer_id, sub_id, weight))

    def compute(self):
        total = sum([x.compute for x in inputs])
        return total

class Node:
    def __init__(self):
        self.function = Function()
        self.output = 0

    def add_input(self, layer_id, sub_id, weight):
        self.function.add_input(layer_id, sub_id, weight)

    def compute(self):
        self.output = function.compute()

class NeuralNet:
    def __init__(self, layers, width):
        self.layers = layers
        self.width = width
        for l in range(layers):
            nodes.append([])
            for w in range(width):
                nodes[l].append(Node())
                if (l == 0):
                    # no connections needed for input layer
                    pass
                else:
                    # connect all nodes from previous layer
                    for w_in in range(width):
                        nodes[l][w].function.add_input(l-1, w_in, 1)

    def read_inputs(self, inputs):
        for w in range(self.width):
            nodes[0][w].output = inputs[w]        

    def compute(self):
        for l in range(1, self.layers):
            for w in range(self.width):
                nodes[l][w].compute()

    def visual_init(self):
        # initialize pygame
        pygame.init()

        # setup the drawing window
        self.screen = pygame.display.set_mode([500, 500])

        # setup nodes and edges visuals
        self.nodes_init()
        self.edges_init()
        
        # new thread for pygame
        thread = threading.Thread(target=self.pygame_thread)
        thread.start()

    def pygame_thread(self):
        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # Update the visualization
            self.visual_update()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def visual_update(self):
        pass

    def nodes_init(self):
        pass

    def edges_init(self):
        pass