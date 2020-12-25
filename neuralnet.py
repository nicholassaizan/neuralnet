import pygame
import threading
import numpy as np
import random

nodes = []

def get_init_weight(layer_id, layers):
    layer_multiplier = 1 - ((layer_id / layers)/3)
    return random.random()/3 * layer_multiplier

class Circle():
    def __init__(self, screen, x, y, radius, layer_id, sub_id):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.layer_id = layer_id
        self.sub_id = sub_id

    def get_value(self):
        return nodes[self.layer_id][self.sub_id].output
    
    def draw(self):
        value = self.get_value()
        if (value > 0.5):
            color = (0, 255, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.circle(self.screen, color, (self.x, self.y), self.radius)

class Edge():
    def __init__(self, screen, pos1, pos2, width, layer_id, sub_id):
        self.screen = screen
        self.pos1 = pos1
        self.pos2 = pos2
        self.width = width
        self.layer_id = layer_id
        self.sub_id = sub_id
    
    def get_value(self):
        return nodes[self.layer_id][self.sub_id].output
    
    def draw(self):
        value = self.get_value()
        if (value > 0.5):
            color = (0, 255, 0)
        else:
            color = (100, 100, 100)
        pygame.draw.line(self.screen, color, self.pos1, self.pos2, self.width)

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
        pre_total = sum([x.compute() for x in self.inputs])
        total = 1/(1 + np.exp(50 * (-(pre_total - 0.5))))
        print(f"pre_total: {pre_total}, total: {total}")
        return total

class Node:
    def __init__(self, is_input = False):
        self.is_input = is_input
        self.function = Function()
        self.output = 0

    def add_input(self, layer_id, sub_id, weight):
        self.function.add_input(layer_id, sub_id, weight)

    def compute(self):
        if (self.is_input == False):
            self.output = self.function.compute()

class NeuralNet:
    def __init__(self, layers, width):
        self.layers = layers
        self.width = width
        for l in range(layers):
            nodes.append([])
            for w in range(width):
                if (l == 0):
                    is_input = True
                else:
                    is_input = False
                nodes[l].append(Node(is_input))
                print(f"Spawning Node ({l},{w})")
                if (l == 0):
                    # no connections needed for input layer
                    pass
                else:
                    # connect all nodes from previous layer
                    for w_in in range(width):
                        print(f"Spawning Connections ({l-1},{w_in})->({l},{w})")
                        nodes[l][w].function.add_input(l-1, w_in, get_init_weight(l, self.layers))

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
        self.screen_scale = 100
        self.screen_width = 16 * self.screen_scale
        self.screen_height = 9 * self.screen_scale
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

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
            self.screen.fill((30, 30, 30))

            # Update the visualization
            self.visual_update()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def visual_update(self):
        for node_visual in self.node_visuals:
            node_visual.draw()
        for edge_visual in self.edge_visuals:
            edge_visual.draw()

    def nodes_init(self):
        x_spacing = self.screen_width / (self.layers + 1)
        y_spacing = self.screen_height / (self.width + 1)
        node_radius = min(x_spacing,y_spacing) / 5

        self.node_visuals = []
        self.edge_visuals = []

        for x in range(self.layers):
            for y in range(self.width):
                x_pos = (x+1) * x_spacing
                y_pos = (y+1) * y_spacing
                print(f"Adding Node Visual ({x},{y})")
                new_node_visual = Circle(self.screen, x_pos, y_pos, node_radius, x, y)
                self.node_visuals.append(new_node_visual)
                
                # get relevant node
                node = nodes[x][y]
                for node_input in node.function.inputs:
                    prev_x = node_input.layer_id
                    prev_y = node_input.sub_id
                    print(f"Adding Edge Visual ({prev_x},{prev_y})->({x},{y})")
                    prev_x_pos = (prev_x+1) * x_spacing
                    prev_y_pos = (prev_y+1) * y_spacing
                    new_edge_visual = Edge(self.screen, (prev_x_pos+node_radius,prev_y_pos), (x_pos-node_radius,y_pos), 2, prev_x, prev_y)
                    self.edge_visuals.append(new_edge_visual)

    def edges_init(self):
        pass