import random
import math
import pygame
import numpy as np

PI = math.pi

MAX_ANGULAR_VEL = 2*PI / 100
MAX_VEL = 100
MAX_ACCEL = 10
MAX_BRAKE = 20


class Car():
    def __init__(self, screen, color, start_pos):
        self.screen = screen
        self.start_pos = start_pos
        self.reset()
        self.color = self.__get_rgb__(color)

    def pedals(self):
        processed_command = (self.accel_command - 0.5) * 0.1

        if (processed_command < 0):
            self.vel += (MAX_BRAKE * processed_command)
        else:
            self.vel += (MAX_ACCEL * processed_command * (1 - (self.vel / MAX_VEL)))

        if (self.vel > MAX_VEL):
            self.vel = MAX_VEL
        elif (self.vel < 0):
            self.vel = 0

    def move(self, time_scale):
        if (self.stopped is False):
            delta_x = self.vel * math.cos(self.angle) * time_scale
            delta_y = self.vel * math.sin(self.angle) * time_scale
            self.x += delta_x
            self.y -= delta_y

            processed_command = 2*(self.steer_command - 0.5) * MAX_ANGULAR_VEL
            self.angle += self.steering_physics(processed_command, time_scale)

            self.odometer += self.vel

    def steering_physics(self, command, time_scale):
        # Distance between axis (L) = 4m
        L = 4

        # Turning radius
        turn_radius = L / (math.tan(command))

        # Cars turns this amount
        delta_angle = self.vel * time_scale / turn_radius

        # Centripedal force
        mass = 1000
        force = mass * self.vel**2 / turn_radius
        force_ratio = force / (mass * MAX_VEL**2 / turn_radius)
        slip_ratio = np.clip(force_ratio * 2.5, 0, 0.75)
        delta_angle *= (1-slip_ratio)

        return delta_angle

    def tick(self, time_scale):
        self.ticks += 1
        self.move(time_scale)
        self.pedals()

    def control(self, steer, accel):
        self.steer_command = steer
        self.accel_command = accel

    def reset(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.vel = 0
        self.angle = 0
        self.accel_command = 0.5
        self.steer_command = 0.5
        self.odometer = 0
        self.stopped = True
        self.ticks = 0
        self.winner = False

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def draw(self):
        size_multiplier = 1
        if (self.winner is True):
            size_multiplier = 2
        vehicle_width = 6 * size_multiplier
        vehicle_length = 10 * size_multiplier
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


class Ray():
    def __init__(self, screen, pos1, pos2):
        self.screen = screen
        self.pos1 = pos1
        self.pos2 = pos2

    def draw(self):
        pygame.draw.line(self.screen, (150, 0, 0), self.pos1, self.pos2)


class Race():
    def __init__(self, screen, num_cars, track_num, time_scale=1):
        self.screen = screen
        self.num_cars = num_cars
        self.track = self.__spawn_track__(track_num)
        self.cars = self.__spawn_cars__()
        self.rays = []
        self.time_scale = time_scale

    def __spawn_cars__(self):
        cars = []
        for n in range(self.num_cars):
            colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'purple']
            color = random.choice(colors)
            cars.append(Car(self.screen, color, self.start_point))
        return cars

    def __spawn_track__(self, track_num):
        width, height = self.screen.get_width(), self.screen.get_height()
        parts = []
        if (track_num == 1):
            parts.append(Track180Turn(self.screen, (width/4, height/2), 100, 200, 'w'))
            parts.append(Track180Turn(self.screen, (width*3/4, height/2), 100, 200, 'e'))
            parts.append(TrackStraight(self.screen, (width/4, height/2-200), (width*3/4, height/2-100)))
            parts.append(TrackStraight(self.screen, (width/4, height/2+100), (width*3/4, height/2+200)))
            self.start_point = (width/2, height/2+150)
        elif (track_num == 2):
            parts.append(Track180Turn(self.screen, (300, 300), 100, 200, 'n'))
            parts.append(Track180Turn(self.screen, (600, 300), 100, 200, 's'))
            parts.append(Track90Turn(self.screen, (900, 300), 100, 200, 'nw'))
            parts.append(TrackStraight(self.screen, (900, 100), (1100, 200)))
            parts.append(Track90Turn(self.screen, (1100, 500), 300, 400, 'ne'))
            parts.append(Track90Turn(self.screen, (1300, 500), 100, 200, 'se'))
            parts.append(TrackStraight(self.screen, (300, 600), (1300, 700)))
            parts.append(Track90Turn(self.screen, (300, 500), 100, 200, 'sw'))
            parts.append(TrackStraight(self.screen, (100, 300), (200, 500)))
            self.start_point = (300, 150)
        return parts

    def on_track(self, pos):
        result = False
        for part in self.track:
            if (part.on_track(pos) is True):
                result = True
        return result

    def timeout(self, distance, ticks):
        if (ticks > 100):
            if (ticks > 500):
                if (distance <= 10):
                    return True
            if (distance <= 1):
                return True
        return False

    def start_race(self):
        for car in self.cars:
            car.start()

    def game_tick(self):
        sensor_readings = []
        stopped = [False] * len(self.cars)
        for i in range(len(self.cars)):
            car = self.cars[i]
            car.tick(self.time_scale)
            pos = (car.x, car.y)

            s1, s2, s3, s4, s5, = 0, 0, 0, 0, 0

            if (self.on_track(pos) is False):
                car.stop()
                stopped[i] = True
            elif (self.timeout(car.odometer, car.ticks) is True):
                car.stop()
                stopped[i] = True
            else:
                s1 = self.sensor_processing(self.sense_distance(pos, car.angle + PI/2), 100)
                s2 = self.sensor_processing(self.sense_distance(pos, car.angle + PI/4), 150)
                s3 = self.sensor_processing(self.sense_distance(pos, car.angle), 300)
                s4 = self.sensor_processing(self.sense_distance(pos, car.angle - PI/4), 150)
                s5 = self.sensor_processing(self.sense_distance(pos, car.angle - PI/2), 150)

            speed = 1 - math.e**(-15 * car.vel / MAX_VEL)

            sensor_readings.append([s1, s2, s3, s4, s5, speed])

        return sensor_readings, stopped

    def sensor_processing(self, readings, distance_scaler):
        return math.e**(-1 * readings / distance_scaler)

    def sense_distance(self, pos, angle):
        search_interval = 5
        distance = 0
        beam = [pos[0], pos[1]]
        while (self.on_track(beam) is True):
            beam[0] += search_interval * math.cos(angle)
            beam[1] -= search_interval * math.sin(angle)
            distance += search_interval
        #self.rays.append(Ray(self.screen, pos, beam))
        return distance

    def get_on_track_distance(self, index):
        distance = self.cars[index].odometer
        pos, angle = (self.cars[index].x, self.cars[index].y), self.cars[index].angle
        timeout = 500
        while (self.on_track(pos) is False):
            if (timeout <= 0):
                return 0
            timeout -= 1
            delta_x = -1 * math.cos(angle)
            delta_y = -1 * math.sin(angle)
            pos = (delta_x + pos[0], delta_y + pos[1])
            distance -= 1
        return distance

    def all_stopped(self):
        result = True
        for car in self.cars:
            if (car.stopped is False):
                result = False
                break
        return result

    def get_fitness(self, index):
        distance = self.get_on_track_distance(index)
        return distance

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

    def set_winner(self, index):
        if (self.cars[index].winner is True):
            self.cars[index].winner = False
        else:
            self.cars[index].winner = True

    def select_winner(self, pos):
        x1, y1 = pos[0], pos[1]
        closest_dist = self.screen.get_width()
        closest_index = 0
        for car_id in range(len(self.cars)):
            x2, y2 = self.cars[car_id].x, self.cars[car_id].y
            dist = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
            if (dist < closest_dist):
                closest_dist = dist
                closest_index = car_id

        self.set_winner(closest_index)

        return closest_index

    def get_winners(self):
        winners = []
        for car_id in range(len(self.cars)):
            car = self.cars[car_id]
            if (car.winner is True):
                winners.append(car_id)
        return winners

    def reset(self):
        for car in self.cars:
            car.reset()

    def draw(self):
        for part in self.track:
            part.draw()
        for ray in self.rays:
            ray.draw()
        self.rays = []
        for car in self.cars:
            car.draw()
