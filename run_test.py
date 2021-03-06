import time
import pygame
import numpy as np
from neuralnet import Pile
from cars import Race
from neuralnet import message_display


force = False


def force_new_gen():
    global force
    if (force is True):
        force = False
        return True
    return False


# Set NN parameters
LAYERS = 7
WIDTHS = (6, 6, 6, 6, 6, 6, 2)

# Create NNs
GROUP_SIZE = 25
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
pile.visual_init(screen, min(GROUP_SIZE, 7))

# Initialize application
TRACK_NUM = 2
TIME_SCALE = 0.5
race = Race(screen, GROUP_SIZE, TRACK_NUM, time_scale=TIME_SCALE)

fresh = True
race_started = False

# Run until the user asks to quit
running = True
outputs = [[]]
while(running):
    # Fill the background with grey
    screen.fill((30, 30, 30))

    # Application update
    sensor_readings = [[0] * WIDTHS[0]] * GROUP_SIZE
    if (fresh is False):
        # Let neural nets control cars
        for i in range(len(race.cars)):
            steer, accel = outputs[i][0], outputs[i][1]
            race.cars[i].control(steer, accel)

        # Start the cars
        if (race_started is False):
            race.start_race()
            race_started = True

        # Periodically progress race
        sensor_readings, stopped_cars = race.game_tick()
        race.draw()

    # Process neural net inputs
    pile.set_inputs(sensor_readings)
    pile.compute()
    outputs = pile.get_outputs()

    if (fresh is False):
        # Update the NN visualization
        pile.visual_update(stopped_cars)

    # Display application controls
    message_display(screen, 'next generation: <SPACE>', 90, 20, 12)
    message_display(screen, 'select parents: <MOUSE_1>', 93, 34, 12)
    message_display(screen, 'increase mutations: <UP>', 88, 48, 12)
    message_display(screen, 'decrease mutations: <DOWN>', 100, 62, 12)

    # Flip the display
    pygame.display.flip()

    if (fresh is False):
        # Check if all cars are done or if next gen was forced
        new_gen = force_new_gen()
        if (new_gen is True):
            # get best genes
            fittest_car_index = race.get_fittest()[0]
            fittest_indeces = race.get_winners()

            if (fittest_indeces == []):
                fittest_indeces.append(fittest_car_index)

            # make mutations of best genes
            pile.new_gen_from_fittest(fittest_indeces)

            # reset cars
            race.reset()

            # start cars
            race_started = False

    # Need to produce outputs before we can start controlling cars
    if (fresh is True):
        fresh = False

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                force = True
            if event.key == pygame.K_UP:
                pile.mutation_multiplier = np.clip(pile.mutation_multiplier + 0.05, 0, 1)
            if event.key == pygame.K_DOWN:
                pile.mutation_multiplier = np.clip(pile.mutation_multiplier - 0.05, 0, 1)
        mouse_click = pygame.mouse.get_pressed()
        if (mouse_click[0] is True):
            race.select_winner(pygame.mouse.get_pos())

    if running is True:
        time.sleep(0.033)

# Done! Time to quit.
pygame.quit()
