import gym
from gym import error, spaces, utils
from gym.utils import seeding
from random import random

class SongEnv(gym.env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
      self.currentSong = random.randint(1, 101)
      self.targetSong = random.randint(1, 101)
      while currentSong == targetSong:
          targetSong = random.randint(1, 101)


      self.action_space = spaces.Discrete(2)


  def nextSong(self):
      if self.currentSong == 100:
          self.currentSong = 1
      else:
          self.currentsong += 1

  def randomSong(self):
      self.currentSong = random.randint(1, 101)

  def isTerminalState(self, state):
      return state == targetSong

  def step(self, action):
      resultState = 0
      if action == 0:
          nextSong()
          resultState = currentSong
      else:
          randomSong()
          resultState = currentSong

      reward = -1 if not self.isTerminalState(resultState) else 0

      return resultState, reward, self.isTerminalState(self.currentSong)





