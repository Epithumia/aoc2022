from queue import SimpleQueue

from parse import parse


def day18():
    with open('../input/input18.txt', 'r') as f:
        data = f.read().splitlines()

    droplet = Droplet()
    for row in data:
        x, y, z = parse('{:d},{:d},{:d}', row)
        droplet.add_cube((x, y, z))

    print('Part 1:', droplet.surface())

    print('Part 2:', droplet.outside_surface())


class Droplet(object):
    def __init__(self):
        self.cubes = dict()
        self.bubbles = dict()

    def add_cube(self, coords, bubble=False):
        x, y, z = coords
        c = Cube(x, y, z)
        if bubble:
            add_to = self.bubbles
        else:
            add_to = self.cubes
        if (x - 1, y, z) in add_to:
            c.add_neighbor(add_to[(x - 1, y, z)])
            add_to[(x - 1, y, z)].add_neighbor(c)
        if (x + 1, y, z) in add_to:
            c.add_neighbor(add_to[(x + 1, y, z)])
            add_to[(x + 1, y, z)].add_neighbor(c)
        if (x, y - 1, z) in add_to:
            c.add_neighbor(add_to[(x, y - 1, z)])
            add_to[(x, y - 1, z)].add_neighbor(c)
        if (x, y + 1, z) in add_to:
            c.add_neighbor(add_to[(x, y + 1, z)])
            add_to[(x, y + 1, z)].add_neighbor(c)
        if (x, y, z - 1) in add_to:
            c.add_neighbor(add_to[(x, y, z - 1)])
            add_to[(x, y, z - 1)].add_neighbor(c)
        if (x, y, z + 1) in add_to:
            c.add_neighbor(add_to[(x, y, z + 1)])
            add_to[(x, y, z + 1)].add_neighbor(c)
        add_to[coords] = c

    def surface(self):
        return sum([c.surface() for c in self.cubes.values()])

    def bubble_surface(self):
        return sum([c.surface() for c in self.bubbles.values()])

    def get_bounds(self):
        x_min, x_max = 1e7, 0
        y_min, y_max = 1e7, 0
        z_min, z_max = 1e7, 0
        for coords in self.cubes.keys():
            x, y, z = coords
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
            z_min = min(z_min, z)
            z_max = max(z_max, z)
        return x_min, x_max, y_min, y_max, z_min, z_max

    def add_bubbles(self):
        x_min, x_max, y_min, y_max, z_min, z_max = self.get_bounds()

        for x in range(x_min - 1, x_max + 1):
            for y in range(y_min - 1, y_max + 1):
                for z in range(z_min - 1, z_max + 1):
                    if (x, y, z) not in self.cubes.keys():
                        self.add_cube((x, y, z), True)
        return x_min, y_min, z_min

    def outside_surface(self):
        x_min, y_min, z_min = self.add_bubbles()
        queue = SimpleQueue()
        queue.put((x_min - 1, y_min - 1, z_min - 1))
        while not queue.empty():
            x, y, z = queue.get()
            if (x, y, z) in self.bubbles:
                b = self.bubbles.pop((x, y, z))
                for n in b.neighbors:
                    n.remove_neighbor(b)
                    queue.put((n.x, n.y, n.z))
                b.neighbors.clear()

        return self.surface() - self.bubble_surface()


class Cube(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbors = set()

    def add_neighbor(self, n):
        self.neighbors.add(n)

    def remove_neighbor(self, n):
        self.neighbors.remove(n)

    def surface(self):
        return 6 - len(self.neighbors)
