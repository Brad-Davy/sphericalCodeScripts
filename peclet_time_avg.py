import numpy as np
import matplotlib.pyplot as plt

file='vel_energy.dat'
timeAverage = 2000
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

problemIdx, resetTime = find_problem_idx()
print('The Peclet number is: {:.4f}'.format(np.average(peclet[-timeAverage:])))
print('The STD was: {:.4f}'.format(np.std(peclet[-timeAverage:])))

