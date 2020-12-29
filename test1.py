import time
import random
import pygame
from neuralnet import Pile
from cars import Race

# Set NN parameters
LAYERS = 3
WIDTHS = (3, 4, 2)

# Create NNs
GROUP_SIZE = 6
pile = Pile(GROUP_SIZE, LAYERS, WIDTHS)

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
pile.visual_init(screen)

# Initialize application
race = Race(screen, 6)

fresh = True
race_started = False

# Run until the user asks to quit
running = True
while(running):
    # Fill the background with grey
    screen.fill((30, 30, 30))

    # Application update
    if (fresh is False):
        # Let neural nets control cars
        for i in range(len(race.cars)):
            left, right = outputs[i][0], outputs[i][1]
            race.cars[i].control(left, right)

        # Start the cars
        if (race_started is False):
            race.start_race()
            race_started = True

        # Periodically start race
        race.game_tick()
        race.draw()

    # Process neural net inputs
    pile.set_inputs([[random.random() for i in range(WIDTHS[0])]] * GROUP_SIZE)
    pile.compute()
    outputs = pile.get_outputs()

    # Need to produce outputs before we can start controlling cars
    if (fresh is True):
        fresh = False

    # Update the NN visualization
    pile.visual_update()

    # Flip the display
    pygame.display.flip()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if running is True:
        time.sleep(0.05)

# Done! Time to quit.
pygame.quit()
