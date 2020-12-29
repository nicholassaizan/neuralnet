import random
import math
import pygame

PI = math.pi

MAX_ANGULAR_VEL = 2*PI / 20
MAX_VEL = 5


class Car():
    def __init__(self, screen, color, start_pos):
        self.screen = screen
        self.start_pos = start_pos
        self.reset()
        self.color = self.__get_rgb__(color)

    def translate(self):
        delta_x = self.vel * math.cos(self.angle)
        delta_y = self.vel * math.sin(self.angle)
        self.x += delta_x
        self.y -= delta_y
        self.odometer += self.vel

    def rotate(self):
        if (self.vel > 0):
            self.angle += MAX_ANGULAR_VEL * (self.left_command - self.right_command)
            self.angle %= (2 * PI)

    def tick(self):
        self.rotate()
        self.translate()

    def control(self, left, right):
        self.left_command = left
        self.right_command = right

    def reset(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.vel = 0
        self.angle = 0
        self.odometer = 0

    def start(self):
        self.vel = MAX_VEL

    def stop(self):
        self.vel = 0

    def draw(self):
        vehicle_width = 6
        vehicle_length = 10
        left = self.x - (vehicle_width/2)
        top = self.y - (vehicle_length/2)
        rect = pygame.Rect(left, top, vehicle_width, vehicle_length)
        pygame.draw.rect(self.screen, self.color, rect)

    def __get_rgb__(self, color):
        if (color == 'red'):
            rgb = (255, 0, 0)
        elif (color == 'yellow'):
            rgb = (255, 255, 0)
        elif (color == 'green'):
            rgb = (0, 255, 0)
        elif (color == 'cyan'):
            rgb = (0, 255, 255)
        elif (color == 'blue'):
            rgb = (0, 0, 255)
        elif (color == 'purple'):
            rgb = (255, 0, 255)
        else:
            rgb = (255, 255, 255)
        return rgb


class TrackStraight():
    def __init__(self, screen, pos1, pos2):
        self.screen = screen
        self.color = (100, 100, 100)
        self.pos1 = pos1
        self.pos2 = pos2
        self.width = self.pos2[0] - self.pos1[0]
        self.height = self.pos2[1] - self.pos1[1]

    def collision(self, pos):
        return False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.pos1[0], self.pos1[1], self.width, self.height))


class Track90Turn():
    def __init__(self, screen, center, inner_radius, outer_radius, direction):
        self.screen = screen
        self.color = (100, 100, 100)
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.rect = (center[0]-outer_radius, center[1]-outer_radius, 2*outer_radius, 2*outer_radius)
        self.__init_angles__(direction)
        self.width = outer_radius - inner_radius

    def __init_angles__(self, direction):
        if (direction == 'nw'):
            self.start_angle = PI/2
            self.stop_angle = PI
        elif (direction == 'sw'):
            self.start_angle = PI
            self.stop_angle = -PI/2
        elif (direction == 'se'):
            self.start_angle = -PI/2
            self.stop_angle = 0
        else:
            self.start_angle = 0
            self.stop_angle = PI/2

    def collision(self, pos):
        return False

    def draw(self):
        pygame.draw.arc(self.screen, self.color, self.rect, self.start_angle, self.stop_angle, self.width)


class Track180Turn():
    def __init__(self, screen, center, inner_radius, outer_radius, direction):
        self.screen = screen
        self.color = (100, 100, 100)
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.rect = (center[0]-outer_radius, center[1]-outer_radius, 2*outer_radius, 2*outer_radius)
        self.__init_angles__(direction)
        self.width = outer_radius - inner_radius

    def __init_angles__(self, direction):
        if (direction == 'n'):
            self.start_angle = 0
            self.stop_angle = PI
        elif (direction == 'w'):
            self.start_angle = PI/2
            self.stop_angle = -PI/2
        elif (direction == 's'):
            self.start_angle = PI
            self.stop_angle = 0
        else:
            self.start_angle = -PI/2
            self.stop_angle = PI/2

    def collision(self, pos):
        return False

    def draw(self):
        pygame.draw.arc(self.screen, self.color, self.rect, self.start_angle, self.stop_angle, self.width)


class Race():
    def __init__(self, screen, num_cars):
        self.screen = screen
        self.num_cars = num_cars
        self.start_point = (self.screen.get_width()/2, self.screen.get_height()/2+150)
        self.cars = self.__spawn_cars__()
        self.track = self.__spawn_track__()

    def __spawn_cars__(self):
        cars = []
        for n in range(self.num_cars):
            colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'purple']
            color = random.choice(colors)
            cars.append(Car(self.screen, color, self.start_point))
        return cars

    def __track_turns__(self):
        turns = []
        turns.append(Track180Turn(self.screen, (self.screen.get_width()/4, self.screen.get_height()/2), 100, 200, 'w'))
        turns.append(Track180Turn(self.screen, (self.screen.get_width()*3/4, self.screen.get_height()/2), 100, 200, 'e'))
        return turns

    def __track_straights__(self):
        straights = []
        straights.append(TrackStraight(self.screen, (self.screen.get_width()/4, self.screen.get_height()/2-200), (self.screen.get_width()*3/4, self.screen.get_height()/2-100)))
        straights.append(TrackStraight(self.screen, (self.screen.get_width()/4, self.screen.get_height()/2+100), (self.screen.get_width()*3/4, self.screen.get_height()/2+200)))
        return straights

    def __spawn_track__(self):
        track = []
        track += self.__track_turns__()
        track += self.__track_straights__()
        return track

    def collision(self, pos):
        result = False
        for part in self.track:
            if (part.collision(pos) is True):
                result = True
        return result

    def start_race(self):
        for car in self.cars:
            car.start()

    def game_tick(self):
        for car in self.cars:
            car.tick()
            pos = (car.x, car.y)
            if (self.collision(pos)):
                car.stop()

    def reset(self):
        for car in self.cars:
            car.reset()

    def draw(self):
        for part in self.track:
            part.draw()
        for car in self.cars:
            car.draw()
