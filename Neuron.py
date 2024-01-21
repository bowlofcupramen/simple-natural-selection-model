"""A neuron"""
import math


class Neuron(object):
    """A neuron"""

    def __init__(self, typ):
        self.typ = typ
        self.inp = 0

    def input(self, val):
        """a"""
        if self.typ == 0:
            self.inp = val
        else:
            self.inp += val

    def output(self):
        """a"""
        if self.typ == 0:
            return self.inp
        else:
            return math.tanh(self.inp)
