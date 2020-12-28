import random
import math
import pygame

PI = math.pi

MAX_ANGULAR_VEL = 2*PI / 40
MAX_VEL = 5


class Car():
    def __init__(self, screen, color):
        self.screen = screen
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
        self.x = 0
        self.y = 0
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
        pygame.draw.rect(screen, self.color, rect)

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


class Race():
    def __init__(self, screen, num_cars):
        self.screen = screen
        self.num_cars = num_cars
        self.cars = self.__spawn_cars__()
        self.track = self.__spawn_track__()

    def __spawn_cars__(self):
        cars = []
        for n in range(self.num_cars):
            colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'purple']
            color = random.choice(colors)
            cars.append(Car(self.screen, color))
        return cars

    def __spawn_track__(self):
        pass

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
        for car in self.cars:
            car.draw()
