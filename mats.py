import pygame
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diff = (1,1,1), spec = 1.0, ks = 0.0, ior=1.0, mattipo=OPAQUE, txtu=None):
        self.diff = diff
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.mattipo = mattipo
        self.txtu = txtu

def glass():
    return Material(diff=(0.9, 0.9, 0.9), spec=64, ks=0.15, ior=1.5, mattipo=TRANSPARENT)
def window():
    return Material(diff=(0.4, 0.4, 0.4), spec=64, ks=0.2, mattipo=REFLECTIVE)
def mirror():
    return Material(diff=(0.9, 0.9, 0.9), spec=64, ks=0.2, mattipo=REFLECTIVE)
def stone():
    return Material(diff=(0.45,0.45,0.45), spec=6, ks=0.05, mattipo=TRANSPARENT)
def star():
    return Material(diff=(0.9, 0.9, 0.9), spec=64, ks=0.2, mattipo=REFLECTIVE)
def blackhole():
    return Material(diff=(0.1, 0.1, 0.1), spec=64, ks=0.2, mattipo=TRANSPARENT)
def bhhalo():
    return Material(diff=(0.2, 0.2, 0.2), spec=64, ks=0.2, mattipo=REFLECTIVE)
def satelite():
    return Material(diff=(0.9, 0.9, 0.9), spec=64, ks=0.1, mattipo=REFLECTIVE)