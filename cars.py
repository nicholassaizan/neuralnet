import random
import math
import pygame

PI = math.pi

MAX_ANGULAR_VEL = 2*PI / 30
MAX_VEL = 100
MAX_ACCEL = 2
MAX_BRAKE = 2


class Car():
    def __init__(self, screen, color, start_pos):
        self.screen = screen
        self.start_pos = start_pos
        self.reset()
        self.color = self.__get_rgb__(color)

    def pedals(self):
        self.vel += ((MAX_ACCEL * self.gas) - (MAX_BRAKE * self.brake))
        if (self.vel > MAX_VEL):
            self.vel = MAX_VEL
        if (self.vel < 0):
            self.vel = 0

    def translate(self):
        if (self.stopped is False):
            delta_x = self.vel * math.cos(self.angle)
            delta_y = self.vel * math.sin(self.angle)
            self.x += delta_x
            self.y -= delta_y
            self.odometer += self.vel

    def rotate(self):
        if (self.stopped is False):
            self.angle += MAX_ANGULAR_VEL * (self.left_command - self.right_command)
            self.angle %= (2 * PI)

    def tick(self):
        self.ticks += 1
        self.rotate()
        self.translate()
        self.pedals()

    def control(self, left, right, gas, brake):
        self.left_command = left
        self.right_command = right
        self.gas = gas
        self.brake = brake

    def reset(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.vel = 0
        self.angle = 0
        self.gas = 0
        self.brake = 0
        self.odometer = 0
        self.stopped = True
        self.ticks = 0

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

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

    def on_track(self, pos):
        result = True
        x, y = pos[0], pos[1]
        if ((x < self.pos1[0]) or (y < self.pos1[1]) or (x > self.pos2[0]) or (y > self.pos2[1])):
            result = False
        return result

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
        self.direction = direction
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

    def on_track(self, pos):
        result = True
        x, y = pos[0], pos[1]
        dist = math.sqrt(math.pow((x-self.center[0]), 2) + math.pow((y-self.center[1]), 2))
        if ((dist < self.inner_radius) or (dist > self.outer_radius)):
            result = False
        if (self.direction == 'nw'):
            if ((x > self.center[0]) or (y > self.center[1])):
                result = False
        elif (self.direction == 'sw'):
            if ((x > self.center[0]) or (y < self.center[1])):
                result = False
        elif (self.direction == 'se'):
            if ((x < self.center[0]) or (y < self.center[1])):
                result = False
        else:
            if ((x < self.center[0]) or (y > self.center[1])):
                result = False
        return result

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
        self.direction = direction
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

    def on_track(self, pos):
        result = True
        x, y = pos[0], pos[1]
        dist = math.sqrt(math.pow((x-self.center[0]), 2) + math.pow((y-self.center[1]), 2))
        if ((dist < self.inner_radius) or (dist > self.outer_radius)):
            result = False
        if (self.direction == 'n'):
            if (y > self.center[1]):
                result = False
        elif (self.direction == 'w'):
            if (x > self.center[0]):
                result = False
        elif (self.direction == 's'):
            if (y < self.center[1]):
                result = False
        else:
            if (x < self.center[0]):
                result = False
        return result

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

    def on_track(self, pos):
        result = False
        for part in self.track:
            if (part.on_track(pos) is True):
                result = True
        return result

    def start_race(self):
        for car in self.cars:
            car.start()

    def game_tick(self):
        sensor_readings = []
        for car in self.cars:
            car.tick()
            pos = (car.x, car.y)

            sensor_left, sensor_middle, sensor_right = 0, 0, 0

            if (self.on_track(pos) is False):
                car.stop()
            else:
                sensor_left = self.sensor_processing(self.sense_distance(pos, car.angle + PI/4))
                sensor_middle = self.sensor_processing(self.sense_distance(pos, car.angle))
                sensor_right = self.sensor_processing(self.sense_distance(pos, car.angle - PI/4))

            speed = car.vel / MAX_VEL
            inverse_speed = 1 - speed
            
            sensor_readings.append([sensor_left, sensor_middle, sensor_right, speed, inverse_speed])

        return sensor_readings

    def sensor_processing(self, readings):
        return math.e**(-1 * readings / 100)

    def sense_distance(self, pos, angle):
        search_interval = 5
        distance = 0
        beam = [pos[0], pos[1]]
        while (self.on_track(beam) is True):
            beam[0] += search_interval * math.cos(angle)
            beam[1] -= search_interval * math.sin(angle)
            distance += search_interval
        return distance

    def all_stopped(self):
        result = True
        for car in self.cars:
            if (car.stopped is False):
                result = False
                break
        return result

    def get_fitness(self, index):
        x1, y1, x2, y2 = 5000, 0, 6000, 0.5
        distance = self.cars[index].odometer
        average_speed = self.cars[index].odometer/self.cars[index].ticks
        scaled_speed = distance / MAX_VEL * average_speed
        if (distance < x1):
            fitness = distance * (1 - y1) + scaled_speed * y1
        elif ((distance >= x1) and (distance <= x2)):
            m = (y2 - y1)/(x2 - x1)
            b = (y2 - y1*x2/x1)/(1 - x2)
            f = lambda x, m, b: m*x + b
            fitness = distance * (1 - f(distance, m, b)) + scaled_speed * f(distance, m, b)
        else:
            fitness = distance * 0.5 + scaled_speed * 0.5
        return fitness

    def get_fittest(self):
        best_fitness = 0
        best_index = 0
        for i in range(len(self.cars)):
            fitness = self.get_fitness(i)
            if (fitness > best_fitness):
                best_fitness = fitness
                best_index = i

        distance_to_solution = self.get_distance_to_solution(best_index, best_fitness)
        return best_index, distance_to_solution

    def get_distance_to_solution(self, index, fitness):
        dist = math.e**(-1 * fitness / 10000)
        return dist

    def reset(self):
        for car in self.cars:
            car.reset()

    def draw(self):
        for part in self.track:
            part.draw()
        for car in self.cars:
            car.draw()
