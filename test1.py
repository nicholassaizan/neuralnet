import time
import random
import pygame
from neuralnet import Pile
from cars import Race


force = False


def force_new_gen():
    global force
    if (force is True):
        force = False
        return True
    return False


# Set NN parameters
LAYERS = 3
WIDTHS = (7, 6, 4)

# Create NNs
GROUP_SIZE = 5
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
pile.visual_init(screen, GROUP_SIZE)

# Initialize application
race = Race(screen, GROUP_SIZE)

fresh = True
race_started = False

# Run until the user asks to quit
running = True
while(running):
    # Fill the background with grey
    screen.fill((30, 30, 30))

    # Application update
    sensor_readings = [[0] * WIDTHS[0]] * GROUP_SIZE
    if (fresh is False):
        # Let neural nets control cars
        for i in range(len(race.cars)):
            left, right, gas, brake = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
            race.cars[i].control(left, right, gas, brake)

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

    # Flip the display
    pygame.display.flip()

    if (fresh is False):
        # Check if all cars are done or if next gen was forced
        new_gen = (race.all_stopped() or force_new_gen())
        if (new_gen is True):
            # get best genes
            fittest_car_index, distance_to_solution = race.get_fittest()

            # make mutations of best genes
            pile.new_gen_from_fittest(fittest_car_index, distance_to_solution)

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

    if running is True:
        time.sleep(0.01)

# Done! Time to quit.
pygame.quit()
