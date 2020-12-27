import pygame
import threading
import numpy as np
import random


def get_init_weight(layer_id, layers):
    layer_multiplier = 1 - ((layer_id / layers)/3)
    return random.random() * layer_multiplier


class Circle():
    def __init__(self, screen, x, y, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, value):
        if (value > 0.5):
            color = (0, 255, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.circle(self.screen, color, (self.x, self.y), self.radius)


class Line():
    def __init__(self, screen, pos1, pos2, width):
        self.screen = screen
        self.pos1 = pos1
        self.pos2 = pos2
        self.width = width

    def draw(self, value):
        r = (1 - value) * 100
        g = 100 + (value * 155)
        b = (1 - value) * 100
        color = (r, g, b)
        pygame.draw.line(self.screen, color, self.pos1, self.pos2, self.width)


class Input:
    def __init__(self, weight):
        self.pre_weighted_value = 0
        self.weighted_value = 0
        self.weight = weight

        self.visualization = None

    def compute(self, pre_weighted_value):
        self.pre_weighted_value = pre_weighted_value
        self.weighted_value = self.pre_weighted_value * self.weight
        return self.weighted_value


class Node:
    def __init__(self):
        self.output = 0

        self.visualization = None

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

            for n in range(self.widths[layer]):
                # add a new node to this layer
                self.nodes[layer].append(Node())

    def __init_inputs__(self):
        for layer in range(self.layers):
            # add a new sub-array for this layer
            self.inputs.append([])

            curr_width = self.widths[layer]
            for i in range(curr_width):
                # add a new sub-array for outputs from this node
                self.inputs[layer].append([])

                if (layer == self.layers - 1):
                    continue

                next_width = self.widths[layer+1]
                for j in range(next_width):
                    weight = get_init_weight(layer, self.layers)
                    self.inputs[layer][i].append(Input(weight))

    def set_inputs(self, inputs):
        if (len(inputs) != self.widths[0]):
            Exception("Inputs array len must match width of first layer")

        self.nn_input_args = inputs

    def get_outputs(self):
        values = []
        for n in range(len(self.nodes[-1])):
            values.append(self.nodes[-1][n].output)

        return values

    def get_input_sum(self, layer, layer_sub_id):
        input_sum = 0

        if (layer == 0):
            input_sum = self.nn_input_args[layer_sub_id]

        else:
            for prev in range(self.widths[layer-1]):
                input_sum += self.inputs[layer-1][prev][layer_sub_id].weighted_value

        return input_sum

    def compute(self):
        for layer in range(self.layers):
            for i in range(self.widths[layer]):
                # get sum of inputs for this node
                input_sum = self.get_input_sum(layer, i)

                # compute the output of nodes in this layer
                output = self.nodes[layer][i].compute(input_sum)  # TODO

                # skip setting input values if this is the output layer
                if (layer == self.layers-1):
                    continue

                for j in range(self.widths[layer+1]):
                    # set the input values of outgoing connections
                    self.inputs[layer][i][j].compute(output)

    def visual_init(self, screen):
        # initialize pygame
        pygame.init()

        # setup the drawing window
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        visual_scale = 5
        self.visual_width = self.screen_width / visual_scale
        self.visual_height = self.screen_height / visual_scale
        self.visual_x_offset = self.screen_width - self.visual_width
        self.visual_y_offset = self.screen_height - self.visual_height

        # setup visuals
        self.node_visual_init()
        self.input_visual_init()

        # new thread for pygame
        # thread = threading.Thread(target=self.pygame_thread)
        # thread.start()

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

    def get_visual_position(self, layer, layer_sub_id):
        # Determine proper spacing
        x_spacing = self.visual_width / (self.layers + 1)
        y_spacing = self.visual_height / (max(self.widths) + 1)

        # Determine node radius
        node_radius = min(x_spacing, y_spacing) / 5

        # Determine x position
        x_pos = (layer + 1) * x_spacing + self.visual_x_offset

        # Determine y position
        y_offset = (max(self.widths) - self.widths[layer]) * y_spacing / 2
        y_pos = (layer_sub_id + 1) * y_spacing + y_offset + self.visual_y_offset

        return (x_pos, y_pos, node_radius)

    def node_visual_init(self):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[x])):
                # Get position of visual
                x_pos, y_pos, node_radius = self.get_visual_position(x, y)

                # Instantiate visual
                self.nodes[x][y].visualization = Circle(self.screen, x_pos, y_pos, node_radius)

    def input_visual_init(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[i])):
                for k in range(len(self.inputs[i][j])):
                    # Get first position of visual
                    x1_pos, y1_pos, node_radius = self.get_visual_position(i, j)
                    x1_pos += node_radius
                    # Get second position of visual
                    x2_pos, y2_pos, node_radius = self.get_visual_position(i+1, k)
                    x2_pos -= node_radius
                    self.inputs[i][j][k].visualization = Line(self.screen, (x1_pos, y1_pos), (x2_pos, y2_pos), 2)

    def node_visual_update(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if (self.nodes[i][j].visualization is not None):
                    value = self.nodes[i][j].output
                    self.nodes[i][j].visualization.draw(value)

    def input_visual_update(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[i])):
                for k in range(len(self.inputs[i][j])):
                    if (self.inputs[i][j][k].visualization is not None):
                        value = self.inputs[i][j][k].weighted_value
                        self.inputs[i][j][k].visualization.draw(value)

    def visual_update(self):
        self.node_visual_update()
        self.input_visual_update()
