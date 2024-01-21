"""a"""

import pygame
import secrets
import random
import World
import Thing
import math as a

NUM_GENES = 16
NUM_THINGS = 1000
NUM_NEUTRAL = 4
WORLD_WIDTH = 128
WORLD_HEIGHT = WORLD_WIDTH
DURATION = 100
GENERATION = 100
CELL_SIZE = 6
OFFSET = CELL_SIZE // 2
WORLD = World.World(WORLD_WIDTH, WORLD_HEIGHT, DURATION)
MUTATE_RATE = 0.001
HEX = "0123456789abcdef"


def populate_world(aliv):
    """a"""
    things = []
    for j in range(NUM_THINGS):
        randx = random.randint(0, WORLD_WIDTH - 1)
        randy = random.randint(0, WORLD_WIDTH - 1)
        while WORLD.is_blocked(randx, randy):
            randx = random.randint(0, WORLD_WIDTH - 1)
            randy = random.randint(0, WORLD_WIDTH - 1)
        if len(aliv) == 0:
            genes = []
            for _ in range(NUM_GENES):
                genes.append(secrets.token_hex(4))
        else:
            genes = aliv[j % len(aliv)].genes
            if random.random() < MUTATE_RATE:
                index = random.randint(0, NUM_GENES - 1)
                j = random.randint(0, 7)
                genes[index] = genes[index][0:j] + random.choice(HEX) + genes[index][j + 1:]

        thing = Thing.Thing(genes, NUM_NEUTRAL, WORLD, randx, randy)
        things.append(thing)
        WORLD.grid[randy][randx] = thing
    return things


def draw(objects, scr):
    """a"""
    scr.fill((255, 255, 255))
    for o in objects:
        pygame.draw.circle(
            screen, [0, 0, 0], (o.pos[0] * CELL_SIZE + OFFSET, o.pos[1] * CELL_SIZE + OFFSET), OFFSET, 0)
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((WORLD_WIDTH * CELL_SIZE, WORLD_HEIGHT * CELL_SIZE))

    alive = []
    for i in range(GENERATION):
        stuffs = populate_world(alive)
        alive = []
        draw(stuffs, screen)
        for _ in range(DURATION):
            for stuff in stuffs:
                stuff.update_input_neurons(stuff.pos[0], stuff.pos[1])
                stuff.think()
            draw(stuffs, screen)
        for m in range(WORLD_WIDTH):
            for n in range(WORLD_HEIGHT):
                loc = [m, n]
                dists = [a.dist([0, 127], loc)]
                # dists = [a.dist([WORLD_HEIGHT // 2, WORLD_WIDTH // 2], loc)]
                r = 16
                if WORLD.grid[n][m] != 0 and any([dist <= r for dist in dists]):
                    alive.append(WORLD.grid[n][m])

        WORLD.clear()
