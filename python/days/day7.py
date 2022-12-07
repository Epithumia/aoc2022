def day7():
    with open('../input/input7.txt', 'r') as f:
        data = f.read().split('\n')[:-1]

    fs = Directory('/')
    current = fs
    i = 1

    while i < len(data):
        cmd = data[i]
        if cmd[0] == '$':  # command
            if cmd[2] == 'c':  # cd
                args = cmd.split(' ')
                current = current.cd(args[2])
            else:  # ls
                pass
        elif cmd[0] == 'd':  # dir
            args = cmd.split(' ')
            d = Directory(args[1])
            current.add_node(d)
        else:  # file
            args = cmd.split(' ')
            f = File(args[1], args[0])
            current.add_node(f)
        i += 1

    print("Part 1:", fs.find_size(100000))
    cutoff = fs.size() - 40000000
    dirs = list(filter(lambda c: c[1] > cutoff, sorted(fs.find_dirs(), key=lambda x: x[1])))
    print("Part 2:", dirs[0][1])


class Directory(object):
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.nodes = dict()

    def __repr__(self):
        r = self.name + ":\n"
        for node in self.nodes:
            if isinstance(self.nodes[node], Directory):
                r += " dir " + str(self.nodes[node].size()) + " " + str(self.nodes[node]) + "\n"
            else:
                r += " file " + str(self.nodes[node].size()) + " " + str(self.nodes[node]) + "\n"
        return r

    def add_node(self, node):
        node.parent = self
        self.nodes[node.name] = node

    def size(self):
        if len(self.nodes) > 0:
            return sum([self.nodes[node].size() for node in self.nodes])
        return 0

    def cd(self, dest):
        if dest == '..':
            return self.parent
        return self.nodes[dest]

    def find_size(self, val):
        if self.size() > val:
            return sum([self.nodes[node].find_size(val) for node in self.nodes])
        else:
            return sum([self.nodes[node].find_size(val) for node in self.nodes]) + self.size()

    def find_dirs(self):
        list_dirs = []
        for node in self.nodes:
            if isinstance(self.nodes[node], Directory):
                list_dirs.append((node, self.nodes[node].size()))
                list_dirs.extend(self.nodes[node].find_dirs())
        return list_dirs


class File(object):
    def __init__(self, name, size):
        self.name = name
        self._size = int(size)

    def __repr__(self):
        return self.name

    def size(self):
        return self._size

    def find_size(self, val):
        return 0
