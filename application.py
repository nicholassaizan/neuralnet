from random import shuffle, randrange, randint

# Maze parameters
max_x = 5
max_y = 5
RUR.current_world.small_tiles = False

# display related options
RUR.MAX_STEPS = 2000  # bigger for large mazes
think(30)


def make_filled_maze(w, h):
    '''Creates a maze of size w by h with
       all grid cells surrounded by walls
    '''
    RUR.we.remove_all()
    RUR.vis_world.compute_world_geometry(w, h)
    for i in range(1, w):
        for j in range(1, h):
            RUR.we.toggle_wall(i, j, "east")
            RUR.we.toggle_wall(i, j, "north")
    for i in range(1, w):
        RUR.we.toggle_wall(i, h, "east")
    for j in range(1, h):
        RUR.we.toggle_wall(w, j, "north")
    RUR.rec.record_frame()


def make_maze(w = 16, h = 8, name="maze"):
    '''Adapted from
       http://rosettacode.org/wiki/Maze_generation#Python

       "name" is the value used to save the maze in the
       browser's local storage so that it is available
       if the page is reloaded.
    '''
    make_filled_maze(w, h)
    pause(500)
    vis = [[False] * w + [True] for _ in range(h)] + [[True] * (w + 1)]
    def walk(x, y):
        vis[y][x] = True
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                RUR.we.toggle_wall(x+1, min(y, yy)+1, "north")
            elif yy == y:
                RUR.we.toggle_wall(min(x, xx)+1, y+1, "east")
            RUR.rec.record_frame()
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    reeborg = UsedRobot(randint(1, max_x), randint(1, max_y))
    RUR.we.add_object("star", randint(1, max_x), randint(1, max_y), 1)
    RUR.rec.record_frame()
    RUR.storage.save_world(name)

def turn_right():
    turn_left()
    turn_left()
    turn_left()

make_maze(max_x, max_y)
pause(500)

while not object_here():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()