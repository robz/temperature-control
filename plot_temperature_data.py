import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

import time

current_milli_time = lambda: int(round(time.time() * 1000))

start_time = current_milli_time();

logfilename = "logs/" + str(datetime.datetime.now()) + ".txt"
logfile = open(logfilename, "w")

class AnalogPlot:
  def __init__(self, port, maxLen, setpoint):
      self.ser = serial.Serial(port, 9600)

      self.temps = [0.0]*maxLen
      self.control = deque([0.0]*maxLen)
      self.setpoints = deque([setpoint]*maxLen)
      self.maxLen = maxLen

  def update(self, frameNum, a0, a1, a2):
      try:
          line = self.ser.readline()
          print line
          dt = current_milli_time() - start_time;
          print(str(float(dt) / 1000))
          data = line.split()
          if len(data) == 2:
              [control, temp] = [float(x) for x in data]
              self.temps[frameNum] = temp
              self.control[frameNum] = control * 250

              logfile.write(
                str(datetime.datetime.now()) +
                ":::" +
                str(control) +
                "," +
                str(temp) +
                "\n"
              )
              logfile.flush()

              a0.set_data(range(self.maxLen), self.temps)
              a1.set_data(range(self.maxLen), self.control)
              a2.set_data(range(self.maxLen), self.setpoints)
      except KeyboardInterrupt:
          print('exiting')

      return a0,

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()

def main():
  port = '/dev/cu.usbmodem14411'
  print('reading from serial port %s...' % port)

  num_points = 12000
  setpoint = 190

  # plot parameters
  analogPlot = AnalogPlot(port, num_points, setpoint)

  print('plotting data and logging to %s...' % logfilename)

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, num_points), ylim=(0, 300))
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  a2, = ax.plot([], [])
  anim = animation.FuncAnimation(
    fig,
    analogPlot.update,
    fargs=(a0, a1, a2),
    interval=50
  )

  # show plot
  plt.show()

  # clean up
  analogPlot.close()

  print('exiting.')

# call main
if __name__ == '__main__':
  main()
