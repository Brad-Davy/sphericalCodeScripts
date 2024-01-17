import numpy as np
import matplotlib.pyplot as plt

file='cod_nusselt.dat'
timeAverage = 20000

with open(file, 'r') as f:

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

problemIdx, resetTime = find_problem_idx()
percentageDifference = (abs(np.average(bottomNusselt[-timeAverage:]) - np.average(topNusselt[-timeAverage:])) / np.average(bottomNusselt[-timeAverage:])) * 100
print('The bottom Nusselt number is: {:.4f}'.format(np.average(bottomNusselt[-timeAverage:])))
print('The top Nusselt number is: {:.4f}'.format(np.average(topNusselt[-timeAverage:])))
print('The STD was: {:.4f}'.format(np.std(topNusselt[-timeAverage:])))
print('The percentage differences is: {:.3f}%'.format(percentageDifference))
plt.axvline(time[-timeAverage])
plt.plot(time, topNusselt, label = '$Nu_T$')
plt.plot(time, bottomNusselt, label = '$Nu_B$')
plt.legend(frameon=False, ncol=2)
plt.show()
