#!/usr/bin/env python3
import os
import time
import random

import pygame as pg
import neat

from classes.base import Base
from classes.bird import Bird
from classes.pipe import Pipe

pg.font.init()


WIN_WIDTH = 550
WIN_HEIGHT = 700

BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bg.png')))

STAT_FONT = pg.font.SysFont('comicsans', 50)


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, -100))

    # draws different objects onto the screen
    for pipe in pipes:
        pipe.draw(win)
    for bird in birds:
        bird.draw(win)
    base.draw(win)

    # renders the font
    text = STAT_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pg.display.update()


def main_loop(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 250))
        g.fitness = 0
        ge.append(g)

    base = Base(630)
    pipes = [Pipe(700)]
    win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()
    score = 0

    run = True
    while run and len(birds) > 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.01

            output = nets[x].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # if the tanh returns greater than 5, the specific bird will jump
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for bird in birds:
                # checks if the bird hits the pipe
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

                # checks if pipe is passed or not
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # after pipe is off the screen, adds pipe to rem list
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        # creates a new pipe and increases score after passing through previous pipe
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 1

            pipes.append(Pipe(700))

        # removes pipes from the rem list after they have left the screen
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            # checks if the bird hits the ground
            if bird.y + bird.img.get_height() > 630 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score)
        clock.tick(30)
        base.move()


# runs program using the config path of the neural net
def run(con_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, con_path)

    pop = neat.Population(config)

    # adds a stat for each generation and its specific species
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main_loop, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
