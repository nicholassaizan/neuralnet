from random import shuffle, randrange


class Maze():
    def __init__(self):
        pass

    def make_maze(w=16, h=8):
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "+  "
                if yy == y:
                    ver[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + ['\n'] + b + ['\n'])
        return s

    def __process_maze__(self, maze_txt):
        parseable = []

        lines = maze_txt.splitlines()
        for line_num in range(len(lines)):
            parseable.append([])
            line_array = [your_string[i:i+3] for i in range(0, len(lines[line_num]), 3)]
            for peice in line_array:
                parseable[line_num].append(peice)

        self.__convert_peices_to_struct__(parseable)

    def __convert_peices_to_struct__(self, peices):
        self.walls = 
        for row in range(len(peices)):
            for col in range(len(row)):
                # Add a cell for this row
                # Process cell horizontal walls
                if row[col] is '+':
                    
                # Process vertical edges
                if line[0] is '|':
                    

