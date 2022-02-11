#!/usr/bin/env python3

import pygame
import time
import numpy as np
import serial
import utils
import copy
import os
import threading

class PumpkinState(threading.Thread):


    def __init__(self):

        threading.Thread.__init__(self)

        self.state_dim = 3
        self.max_size = 100

        self.state = np.zeros(self.state_dim)

        
        self.idx = 0
        self.size = 0
        self.state_history = np.zeros((self.max_size, self.state_dim))

        self.state_serial = serial.Serial('/dev/ttyACM0', 9600)

        self.quit = False

    @property
    def states(self):
        
        state_history = copy.deepcopy(self.state_history)

        states = np.zeros_like(state_history)

        if self.size == self.max_size:
            states = np.vstack([state_history[self.idx:,:],state_history[:self.idx,:]])
        else:
            states = state_history[:self.idx]


        return states

    @property
    def current_state(self):

        return copy.deepcopy(self.state)
    
    def append(self, x):

        self.state_history[self.idx,:] = x

        self.idx = (self.idx + 1)%self.max_size
        self.size = min(self.size+1, self.max_size)


    def update(self):
        
        line = self.state_serial.readline().decode()

        line = line.split(',')
        if len(line) == 3:

            try:
                self.state = np.array([ float(v) for v in line])

                # print("State: ", self.state)

                self.append(self.state)
            except:
                pass

    def run(self):

        while not self.quit:


            self.update()

            


class Pumpkin(object):


    def __init__(self):

        self.pstate = PumpkinState()
        

        self.sound_files = utils.crawl(utils.get_package_path(), "mp3")
        self.sound_files = [ paths for _, paths in self.sound_files.items()]
        print(self.sound_files)

        pygame.mixer.init()

        self.start()

    def start(self):
        self.pstate.start()

    def update(self):

        state = self.pstate.current_state

        # print("Distance: ", state[1])
        if state[1] <= 0.5 and state[1] > 0.0:
            print("Distance is {} - Time to spook!".format(state[1]))
            sid = np.random.randint(0,len(self.sound_files))
            file = self.sound_files[sid]
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

            time.sleep(5)
    


#haunting.mp3
def main():
    

    os.system("Starting up")
    pumpkin = Pumpkin()

    plotter = utils.VisdomLinePlotter(env_name='Pumpkin State')

    while True:

        pumpkin.update()

        states = pumpkin.pstate.states
        
        if len(states) > 0:
            # print("States: ", states[:,0].shape, " - ", states[:,1].shape)
            plotter.plot("distance (m)", "pumpkin self-distance status", "Distance to Pumpkin", states[:,0], states[:,1])


        time.sleep(0.001)

if __name__ == "__main__":
    main()

