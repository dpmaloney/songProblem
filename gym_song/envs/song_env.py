import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random as rand

class SongEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
      self.currentSong = rand.randint(1, 101)
      self.targetSong = rand.randint(1, 101)
      while self.currentSong == self.targetSong:
          self.targetSong = rand.randint(1, 101)


     


  def nextSong(self):
      if self.currentSong == 100:
          self.currentSong = 1
      else:
          self.currentSong += 1

  def randomSong(self):
      self.currentSong = rand.randint(1, 101)

  def isTerminalState(self):
      return self.currentSong == self.targetSong

  def step(self, action):
      resultState = 0
      if action == 0:
          self.nextSong()
          resultState = self.targetSong - self.currentSong
      else:
          self.randomSong()
          resultState = self.targetSong - self.currentSong

      reward = -1 if not self.isTerminalState() else 0

      return abs(resultState), reward, self.isTerminalState(), None

  def reset(self):
      self.currentSong = rand.randint(1, 101)
      self.targetSong = rand.randint(1, 101)
      while self.currentSong == self.targetSong:
          self.targetSong = rand.randint(1, 101)

  def render(self):
      print(self.currentSong)

