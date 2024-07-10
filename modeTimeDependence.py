import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

mypath='.'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
velSpectrumFiles = []
largestNumber = 0
numOfTimeSteps = 330

for lines in onlyfiles:
    if 'vel_spectrum' in lines:
        velSpectrumFiles.append(lines)

for idx,lines in enumerate(velSpectrumFiles):
    fileNumber  = int(lines.split('_')[2].split('.')[0])
    if fileNumber > largestNumber:
        largestNumber = fileNumber
        fileNumberIdx = idx

def findIdx(fileNumbers):
    fileIdx = []
    for number in fileNumbers:
        for idx,lines in enumerate(velSpectrumFiles):
             if number == int(lines.split('_')[2].split('.')[0]):
                fileIdx.append(idx)
    return fileIdx

def returnSpectraFromDataFile(fileName):
    with open(fileName, 'r') as file:
        rawData = file.read().split('\n')
        waveNumbers = []
        values = []
        time = float(rawData[0].split('=')[1])
        for lines in rawData:
            lines = lines.replace('   ', '  ')
            lines = lines.replace('  ', ' ')
            data = lines.split(' ')
            if data[0] == '' and len(data) > 2:
                try:
                    waveNumbers.append(int(data[1]))
                    values.append(float(data[2]))
                except:
                    pass
    return waveNumbers, values, time

def determineNewStartPoint(dns_waveNumbers):
    problemIdx = []
    for idx in range(1, len(dns_waveNumbers)):
        if dns_waveNumbers[idx] < dns_waveNumbers[idx-1]:
            problemIdx.append(idx)

    if len(problemIdx) == 1:
        return problemIdx[0]
    else:
        return problemIdx

def returnMandL(fileName):
    waveNumbers, values, time = returnSpectraFromDataFile(fileName)
    new_start_point = determineNewStartPoint(waveNumbers)
    return waveNumbers[:new_start_point], values[:new_start_point], waveNumbers[new_start_point:], values[new_start_point:], time


def determineTimeSeries(M, mode, time):
    array = []
    for lines in M:
        array.append(lines[mode])
    return [mode  for _,mode  in sorted(zip(time,array))]

fileNumbers = [largestNumber - i for i in range(numOfTimeSteps)]
print(fileNumbers)
fileIdx = findIdx(fileNumbers)

M = []
L = []
T = []

modesToTest = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
timeOfMode = []


for lines in fileIdx:
    waveNumbersL, valuesL, waveNumbersM, valuesM, time = returnMandL(velSpectrumFiles[lines])
    M.append(valuesM)
    L.append(valuesL)
    T.append(time)

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['figure.autolayout'] = True
cm = 1/2.54


figSize = (15*cm, 6*cm)

for modes in modesToTest:
    timeSeries = determineTimeSeries(M, mode=modes, time=T)
    plt.plot(sorted(T), timeSeries, label = 'm={}'.format(modes))


plt.legend(ncol=4,frameon=False)
plt.yscale('log')
plt.savefig('img/modesTimeSeries.svg', dpi=500)
