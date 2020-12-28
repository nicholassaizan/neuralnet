import random
import math

PI = math.pi

MAX_ANGULAR_VEL = 2*PI / 40


class Car():
    def __init__(self, color):
        self.x = 0
        self.y = 0
        self.vel = 0
        self.angle = 0
        self.color = self.__get_rgb__(color)

    def translate(self):
        delta_x = self.vel * math.cos(self.angle)
        delta_y = self.vel * math.sin(self.angle)
        self.x += delta_x
        self.y -= delta_y

    def rotate(self):
        self.angle += MAX_ANGULAR_VEL * (self.left_command - self.right_command)
        self.angle %= (2 * PI)

    def tick(self):
        self.rotate()
        self.translate()

    def control(self, left, right):
        self.left_command = left
        self.right_command = right

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
    def __init__(self, num_cars):
        self.num_cars = num_cars
        self.cars = self.__spawn_cars__()

    def __spawn_cars__(self):
        cars = []
        for n in range(self.num_cars):
            colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'purple']
            color = random.choice(colors)
            cars.append(Car(color))
        return cars

    def game_tick(self):
        for car in self.cars:
            car.tick()
