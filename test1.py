import time
import random
import pygame
from neuralnet import NeuralNet

# Set NN parameters
LAYERS = 4
WIDTHS = (3, 4, 4, 2)

# Create NNs
NN1 = NeuralNet(LAYERS, WIDTHS)
NN2 = NeuralNet(LAYERS, WIDTHS)

# Initialize pygame
pygame.init()

# Setup screen
screen_scale = 100
screen_width_scale = 16
screen_height_scale = 9
screen_width = screen_scale * screen_width_scale
screen_height = screen_scale * screen_height_scale
screen = pygame.display.set_mode([screen_width, screen_height])

# Initialize NN visuals
NN1.visual_init(screen)

# Initialize application
# TODO ...

# Run until the user asks to quit
running = True
while(running):
    # Fill the background with white
    screen.fill((30, 30, 30))

    # ...
    # Do application stuff TODO
    # ...
    pygame.draw.circle(screen, (255, 0, 0), (screen_width/2, screen_height/2), screen_scale/10)

    # Process neural net inputs
    NN1.read_inputs([random.random() for i in range(WIDTHS[0])])
    NN2.read_inputs([random.random() for i in range(WIDTHS[0])])
    NN1.compute()
    NN2.compute()

    # Update the NN visualization
    NN1.visual_update()

    # Flip the display
    pygame.display.flip()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if running is True:
        time.sleep(1)

# Done! Time to quit.
pygame.quit()
