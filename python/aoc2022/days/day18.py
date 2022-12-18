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
        xmin, xmax = 1e7, 0
        ymin, ymax = 1e7, 0
        zmin, zmax = 1e7, 0
        for coords in self.cubes.keys():
            x, y, z = coords
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
            zmin = min(zmin, z)
            zmax = max(zmax, z)
        return xmin, xmax, ymin, ymax, zmin, zmax

    def add_bubbles(self):
        xmin, xmax, ymin, ymax, zmin, zmax = self.get_bounds()

        for x in range(xmin - 5, xmax + 5):
            for y in range(ymin - 5, ymax + 5):
                for z in range(zmin - 5, zmax + 5):
                    if (x, y, z) not in self.cubes.keys():
                        self.add_cube((x, y, z), True)
        return xmin, ymin, zmin

    def outside_surface(self):
        xmin, ymin, zmin = self.add_bubbles()
        queue = SimpleQueue()
        queue.put((xmin - 5, ymin - 5, zmin - 5))
        while not queue.empty():
            x, y, z = queue.get()
            b = self.bubbles.get((x, y, z), Cube(-10, -10, -10))
            neighbors = b.neighbors.copy()
            for n in neighbors:
                n.remove_neighbor(b)
                b.remove_neighbor(n)
                queue.put((n.x, n.y, n.z))
            if b.surface() == 6 and b.x != -10:
                self.bubbles.pop((x, y, z))

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
