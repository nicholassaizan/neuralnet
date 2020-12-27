import pygame
import threading
import numpy as np
import random


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


class Line():
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
    def __init__(self, weight):
        self.pre_weighted_value = 0
        self.weighted_value = 0
        self.weight = weight

    def compute(self, pre_weighted_value):
        self.pre_weighted_value = pre_weighted_value
        self.weighted_value = self.pre_weighted_value * self.weight
        return self.weighted_value


class Node:
    def __init__(self):
        self.output = 0

    def compute(self, input_sum):
        self.output = 1/(1 + np.exp(50 * (-(input_sum - 0.5))))
        return self.output


class NeuralNet:
    def __init__(self, layers, widths):
        # Check inputs
        if (layers < 2):
            Exception("Must be atleast 2 layers")
        if (len(widths) != layers):
            Exception("widths must have a value for each layer")

        # Copy dimensions
        self.layers = layers
        self.widths = widths

        # Declare nodes & inputs
        self.nodes = []
        self.inputs = []

        # Initialize nodes & inputs
        self.__init_nodes__()
        self.__init_inputs__()

        # Initialize misc variables
        self.nn_input_args = [0 for x in range(widths[0])]

    def __init_nodes__(self):
        for layer in range(self.layers):
            # add a new sub-array for this layer
            self.nodes.append([])

            # check if this is the input layer
            if (layer == 0):
                is_input_layer = True
            else:
                is_input_layer = False

            for n in range(len(self.widths[layer])):
                # add a new node to this layer
                self.nodes[layer].append(Node(is_input_layer))

    def __init_inputs__(self):
        for layer in range(self.layers - 1):
            # add a new sub-array for this layer
            self.inputs.append([])

            curr_width = self.widths[layer]
            for i in range(curr_width):
                # add a new sub-array for outputs from this node
                self.inputs[layer].append([])

                next_width = self.widths[layer]
                for j in range(next_width):
                    weight = get_init_weight(layer, self.layers)
                    self.inputs[layer][i].append(Input(weight))

    def read_inputs(self, inputs):
        if (len(inputs) != self.widths[0]):
            Exception("Inputs array len must match width of first layer")

        self.nn_input_args = inputs

    def get_input_sum(self, layer, layer_sub_id):
        input_sum = 0

        if (layer == 0):
            input_sum = self.nn_input_args[layer_sub_id]

        else:
            for prev in range(self.widths[layer-1]):
                input_sum += self.inputs[layer][prev][layer_sub_id].weighted_value

        return input_sum

    def compute(self):
        for layer in range(self.layers):
            for i in range(self.widths[layer]):
                # get sum of inputs for this node
                input_sum = self.get_input_sum(layer, i)

                # compute the output of nodes in this layer
                output = self.nodes[layer][i].compute(input_sum)  # TODO

                # skip setting input values if this is the output layer
                if (layer == self.layers):
                    continue

                for j in range(self.widths[layer+1]):
                    # set the input values of outgoing connections
                    self.inputs[layer][i][j].compute(output)

    def visual_init(self):
        # initialize pygame
        pygame.init()

        # setup the drawing window
        self.screen_scale = 100
        self.screen_width = 16 * self.screen_scale
        self.screen_height = 9 * self.screen_scale
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        # setup visuals
        self.node_visuals_init()
        self.input_visuals_init()
        
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
        y_spacing = self.screen_height / (max(self.widths) + 1)
        node_radius = min(x_spacing,y_spacing) / 5

        for x in range(self.layers):
            for y in range(self.width):
                x_pos = (x+1) * x_spacing
                y_pos = (y+1) * y_spacing
                print(f"Adding Node Visual ({x},{y})")
                new_node_visual = Circle(self.screen, x_pos, y_pos, node_radius, x, y)
                self.node_visuals.append(new_node_visual)
                
                # get relevant node
                node = self.nodes[x][y]
                for node_input in node.function.inputs:
                    prev_x = node_input.layer_id
                    prev_y = node_input.sub_id
                    print(f"Adding Edge Visual ({prev_x},{prev_y})->({x},{y})")
                    prev_x_pos = (prev_x+1) * x_spacing
                    prev_y_pos = (prev_y+1) * y_spacing
                    new_edge_visual = Edge(self.screen, (prev_x_pos+node_radius,prev_y_pos), (x_pos-node_radius,y_pos), 2, prev_x, prev_y)
                    self.edge_visuals.append(new_edge_visual)