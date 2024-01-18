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
from docopt import docopt
from colours import *
import os

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

args = docopt(__doc__)
timeAverage = int(args['--t'])

dataFile='cod_nusselt.dat'

with open(dataFile, 'r') as f:

    data = f.read().split('\n')
    topNusselt = []
    bottomNusselt = []
    time = []

    for line in data:
        line = line.replace('   ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace(' ', '"')
        lineData = line.split('"')
        try:
            time.append(float(lineData[1]))
            topNusselt.append(float(lineData[7]))
            bottomNusselt.append(float(lineData[8]))
        except:
git clone git@github.com:Brad-Davy/sphericalCodeScripts.git            pass

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

problemIdx, resetTime = find_problem_idx()
percentageDifference = (abs(np.average(bottomNusselt[-timeAverage:]) - np.average(topNusselt[-timeAverage:])) / np.average(bottomNusselt[-timeAverage:])) * 100

print('-'*60)
print('The bottom Nusselt number is: {:.4f}'.format(np.average(bottomNusselt[-timeAverage:])))
print('The top Nusselt number is: {:.4f}'.format(np.average(topNusselt[-timeAverage:])))
print('The STD was: {:.4f}'.format(np.std(topNusselt[-timeAverage:])))
print('The percentage differences is: {:.3f}%'.format(percentageDifference))
print('The length of the text files is: {}'.format(len(bottomNusselt)))
print('-'*60)

if os.path.isdir('img') == True:
    pass
else:
    os.system('mkdir img')

fig = plt.figure(figsize=(7.5*cm, 9*cm))
plt.axvline(time[-timeAverage], color = 'black', linestyle='dotted')
plt.plot(time, topNusselt, label = '$Nu_T$', color = CB91_Blue)
plt.plot(time, bottomNusselt, label = '$Nu_B$', color = CB91_Amber)
plt.ylabel('Nu')
plt.xlabel('Time')
plt.legend(frameon=False, ncol=2)
plt.savefig('img/nusselt_time_series.svg', dpi=500)
plt.show()

cwd = os.getcwd()
print('\n')
print('-'*60)
print('Copy to home command for Archer2:')
print('scp -r scbd@login.archer2.ac.uk:'+cwd+'/img .')
print('Copy to home command for Arc4:')
print('scp -r arc4.leeds.ac.uk:'+cwd+'/img .')
print('-'*60)




