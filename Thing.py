"""A thing"""
import Neuron as Neu
import random


class Thing:
    """A thing"""
    dirs = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    def __init__(self, genes, num_neutrals, world, x, y):
        self.genes = genes
        self.age = 0
        self.inputs = []
        self.neutral = []
        self.outputs = []
        self.width = world.get_width()
        self.height = world.get_height()
        self.dir = 0
        self.world = world
        self.connections = [[], [], [], []]
        self.pos = (x, y)
        for _ in range(14):
            self.inputs.append(Neu.Neuron(0))
        for _ in range(num_neutrals):
            self.neutral.append(Neu.Neuron(1))
        for _ in range(7):
            self.outputs.append(Neu.Neuron(2))
        for string in genes:
            d = self.decode(string)
            self.connections[d[0] - 1].append(d)

    def update_input_neurons(self, x, y):
        """a"""
        self.inputs[0].input(min(self.age / self.world.duration, 1.0))
        self.inputs[1].input(random.randint(0, 9))

        perp_blocked = 0
        dir1 = self.dirs[(self.dir + 2) % 8]
        dir2 = self.dirs[(self.dir - 2) % 8]
        if self.world.is_blocked(x + dir1[0], y + dir1[1]):
            perp_blocked += 0.5
        if self.world.is_blocked(x + dir2[0], y + dir2[1]):
            perp_blocked += 0.5

        self.inputs[2].input(perp_blocked)
        self.inputs[3].input(
            1.0 if self.world.is_blocked(x + self.dirs[self.dir][0], y + self.dirs[self.dir][1]) else 0.0)

        self.inputs[4].input(self.world.get_density(x + self.dirs[self.dir][0] + 5, y + self.dirs[self.dir][1] + 5))
        self.inputs[5].input(
            1.0 if self.world.is_blocked(x + self.dirs[self.dir][0] + 5, y + self.dirs[self.dir][1] + 5) else 0.0)

        self.inputs[6].input(self.dirs[self.dir][0])
        self.inputs[7].input(self.dirs[self.dir][1])
        self.inputs[8].input((self.height - y) / self.height)
        self.inputs[9].input((self.width - x) / self.width)
        self.inputs[10].input(x / self.width)
        self.inputs[11].input(y / self.height)
        self.inputs[12].input(
            min((self.height - y) / self.height, (self.width - x) / self.width, y / self.height, x / self.width))
        self.inputs[13].input(self.world.get_density(x, y))

    def decode(self, string):
        """a"""
        binary = bin(int(string, 16))[2:].zfill(32)
        input_typ = int(binary[0])
        output_typ = int(binary[8])
        if input_typ == 0:
            src_id = int('0b' + binary[1:8], 2) % 14
        else:
            src_id = int('0b' + binary[1:8], 2) % len(self.neutral)
        if output_typ == 0:
            out_id = int('0b' + binary[9:16], 2) % 7
        else:
            out_id = int('0b' + binary[9:16], 2) % len(self.neutral)
        weight = int('0b' + binary[16:], 2) / 10000
        if input_typ == 0 and output_typ == 1:
            typ = 1
        elif input_typ == 1 and output_typ == 1:
            typ = 2
        elif input_typ == 0 and output_typ == 0:
            typ = 3
        else:
            typ = 4
        return [typ, src_id, out_id, weight]

    def think(self):
        """a"""
        for i in range(4):
            for connection in self.connections[i]:
                if i == 0:
                    self.neutral[connection[2]].input(self.inputs[connection[1]].output() * connection[3])
                elif i == 1:
                    self.neutral[connection[2]].input(self.neutral[connection[1]].output() * connection[3])
                elif i == 2:
                    self.outputs[connection[2]].input(self.inputs[connection[1]].output() * connection[3])
                else:
                    self.outputs[connection[2]].input(self.neutral[connection[1]].output() * connection[3])
        choice = random.random()
        for i in range(7):
            result = self.outputs[i].output()
            if result != 0 and choice < abs(result):
                self.set_dir(i, result)
                target = (self.pos[0] + self.dirs[self.dir][0], self.pos[1] + self.dirs[self.dir][1])
                blocked = self.world.is_blocked(target[0], target[1])
                if not blocked:
                    if i == 0:
                        nothing = 0
                        nothing += 1
                        # comment line below to disable killing
                        # self.world.kill(target[0], target[1])
                    else:
                        self.world.move(self, target[0], target[1])
                        self.pos = target

    def set_dir(self, i, result):
        """a"""
        if i == 2 and result > 0:
            self.dir = random.randint(0, 7)
        elif i == 3 and result > 0:
            self.dir = self.dir = (self.dir + 4) % 8
        elif i == 4:
            self.dir = (self.dir - (2 if result > 0 else -2)) % 8
        elif i == 5:
            self.dir = 2 if result > 0 else 6
        elif i == 6:
            self.dir = 0 if result > 0 else 4
