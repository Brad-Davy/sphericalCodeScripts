"""Extracts the Nusselt number data from a spherical run.

Usage:
    nusselt_time_avg.py [--t=<averaging time period>]
    nusselt_time_avg.py | --help

Options:
    -h --help                           Display this help message
    --t=<averaging time period>         Averaging time period [default: 500]
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from docopt import docopt
from colours import *

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

file='vel_energy.dat'
args = docopt(__doc__)
timeAverage = int(args['--t'])
Pr = 1

with open(file, 'r') as f:

    data = f.read().split('\n')
    time = []
    peclet = []
    for line in data:
        line = line.replace('   ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace(' ', '"')
        lineData = line.split('"')
        try:
            time.append(float(lineData[1]))
            peclet.append(float(lineData[2]))
        except:
            pass

def find_problem_idx():
    problem_idx = 0
    reset_time = 0
    for idx,t in enumerate(time):
        if t < time[idx-1] and t < 1e-5 and idx != 0:
            print('Current time: {:4e}, Time before: {:.4e}, Index: {}'.format(t, time[idx-1], idx))
            problem_idx = idx
            reset_time = time[idx-1]
    if problem_idx != 0:
        return problem_idx, reset_time

    else:
        return None, None

problemIdx, resetTime = find_problem_idx()

if problemIdx is None:
    print('No problems found in the txt file.')
else:
    time[problemIdx:] = np.array(time[problemIdx:]) + resetTime

peclet = np.sqrt(2*np.array(peclet)/14.59)*Pr
runTime = time[-1] * np.average(peclet[-timeAverage:])
problemIdx, resetTime = find_problem_idx()
print('-'*60)
print('The Peclet number is: {:.4f}'.format(np.average(peclet[-timeAverage:])))
print('The STD was: {:.4f}'.format(np.std(peclet[-timeAverage:])))
print('The run time in convective overturn time is: {:.2f}'.format(runTime))
print('-'*60)

if os.path.isdir('img') == True:
    pass
else:
    os.system('mkdir img')

fig = plt.figure(figsize=(7.5*cm, 9*cm))
plt.plot(time, peclet, color = CB91_Blue)
plt.xlabel('Time')
plt.ylabel('Pe')
plt.savefig('img/peclet_time_series.svg', dpi=500)
