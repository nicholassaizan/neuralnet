import pygame
import numpy as np
import random
import math


white = (255, 255, 255)


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, x, y):
    largeText = pygame.font.Font('freesansbold.ttf', 25)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((x/2), (y/2))
    screen.blit(TextSurf, TextRect)


def get_init_weight(layer_id, layers):
    layer_multiplier = (1 - (layer_id / layers))
    weight = random.uniform(-1, 1) * layer_multiplier
    return weight


class Circle():
    def __init__(self, screen, x, y, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, value, status):
        if (status is True):
            color = (10, 10, 10)
        elif (value > 0.5):
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

    def draw(self, value, status):
        if (status is True):
            color = (0, 0, 0)
        elif (value < 0):
            r = 100 + (-value * 155)
            g = (1 + value) * 100
            b = (1 + value) * 100
            color = (r, g, b)
        else:
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

        self.visual_initialized = False

    def __init_nodes__(self):
        for layer in range(self.layers):
            # add a new sub-array for this layer
            self.nodes.append([])

            for n in range(self.widths[layer]):
                # add a new node to this layer
                self.nodes[layer].append(Node())

    def __init_inputs__(self):
        self.num_inputs = 0
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
                    self.num_inputs += 1

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

    def visual_init(self, screen, visual_id, num_visuals):
        # initialize pygame
        pygame.init()

        self.visual_id = visual_id
        self.num_visuals = num_visuals

        # setup the drawing window
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.visual_width = self.screen_width / self.num_visuals
        self.visual_height = self.screen_height / self.num_visuals
        self.visual_x_offset = self.visual_width * self.visual_id
        self.visual_y_offset = self.screen_height - self.visual_height

        # setup visuals
        self.node_visual_init()
        self.input_visual_init()

        self.visual_initialized = True

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

    def node_visual_update(self, status):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if (self.nodes[i][j].visualization is not None):
                    value = self.nodes[i][j].output
                    self.nodes[i][j].visualization.draw(value, status)

    def input_visual_update(self, status):
        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[i])):
                for k in range(len(self.inputs[i][j])):
                    if (self.inputs[i][j][k].visualization is not None):
                        value = self.inputs[i][j][k].weighted_value
                        self.inputs[i][j][k].visualization.draw(value, status)

    def visual_update(self, status):
        self.node_visual_update(status)
        self.input_visual_update(status)


class Pile():
    def __init__(self, num_nn, layers, widths):
        self.gen_id = 0
        self.nun_nn = num_nn
        self.layers = layers
        self.widths = widths
        self.neural_nets = [NeuralNet(self.layers, self.widths) for i in range(num_nn)]
        self.mutation_multiplier = 0.1

    def visual_init(self, screen, num_visuals):
        self.screen = screen
        for visual_id in range(num_visuals):
            self.neural_nets[visual_id].visual_init(self.screen, visual_id, num_visuals)

    def visual_update(self, statuses):
        for i in range(len(self.neural_nets)):
            if (self.neural_nets[i].visual_initialized is True):
                self.neural_nets[i].visual_update(statuses[i])
        message_display(self.screen, 'generation: ' + str(self.gen_id), self.screen.get_width(), 100)

    def set_inputs(self, inputs):
        for i in range(len(self.neural_nets)):
            self.neural_nets[i].set_inputs(inputs[i])

    def compute(self):
        for nn in self.neural_nets:
            nn.compute()

    def get_outputs(self):
        outputs = [nn.get_outputs() for nn in self.neural_nets]
        return outputs

    def pass_on_genes(self, indeces):
        for i in range(len(self.neural_nets)):
            # don't need to copy to the parent
            if (i in indeces):
                continue

            # copy weights from parents to child
            child_inputs = self.neural_nets[i].inputs
            for layer in range(len(child_inputs)):
                for layer_sub_id in range(len(child_inputs[layer])):
                    for input_sub_id in range(len(child_inputs[layer][layer_sub_id])):
                        # randomly select which parent to copy from
                        index = random.choice(indeces)
                        parent_inputs = self.neural_nets[index].inputs

                        # copy gene from parent
                        self.neural_nets[i].inputs[layer][layer_sub_id][input_sub_id].weight = parent_inputs[layer][layer_sub_id][input_sub_id].weight

    def mutate_children(self, indeces):
        for i in range(len(self.neural_nets)):
            # don't modify the parent
            if (i in indeces):
                continue

            # determine how probable mutations are based on number of inputs
            num_mutations = math.ceil(self.neural_nets[0].num_inputs) * self.multiplier

            # invoke mutations
            for n in range(num_mutations):
                delta = random.uniform(-1, 1) * self.multiplier

                # random select a weight to modify
                nn_inputs = self.neural_nets[i].inputs
                layer = random.choice(range(len(nn_inputs) - 1))
                layer_sub_id = random.choice(range(len(nn_inputs[layer])))
                input_sub_id = random.choice(range(len(nn_inputs[layer][layer_sub_id])))

                # add a mutation to the weight
                old_weight = self.neural_nets[i].inputs[layer][layer_sub_id][input_sub_id].weight
                weight = old_weight + delta
                self.neural_nets[i].inputs[layer][layer_sub_id][input_sub_id].weight = np.clip(weight, -1, 1)

        self.gen_id += 1

    def new_gen_from_fittest(self, indeces):
        self.pass_on_genes(indeces)
        self.mutate_children(indeces)
