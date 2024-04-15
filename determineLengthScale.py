import numpy as np
from os import listdir
from os.path import isfile, join

mypath='.'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

velSpectrumFiles = []
largestNumber = 0
numOfTimeSteps = 40

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
    for numbers in fileNumbers:
        for idx,lines in enumerate(velSpectrumFiles):
            if str(numbers) in lines:
                fileIdx.append(idx)
    return fileIdx

def returnSpectraFromDataFile(fileName):
    with open(fileName, 'r') as file:
        rawData = file.read().split('\n')
        waveNumbers = []
        values = []
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
    return waveNumbers, values

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
    waveNumbers, values = returnSpectraFromDataFile(fileName)
    new_start_point = determineNewStartPoint(waveNumbers)
    return waveNumbers[:new_start_point], values[:new_start_point], waveNumbers[new_start_point:], values[new_start_point:]


fileNumbers = [largestNumber - i for i in range(numOfTimeSteps)]
fileIdx = findIdx(fileNumbers)

M = []
L = []

for lines in fileIdx:
    waveNumbersL, valuesL, waveNumbersM, valuesM = returnMandL(velSpectrumFiles[lines])
    M.append(valuesM)
    L.append(valuesL)

M = np.array(M)
L = np.array(L)

print(np.shape(M))
averageM = np.average(M, axis=0)
averageL = np.average(L, axis=0)
stdM = np.std(np.abs(M), axis=0)
stdL = np.std(np.abs(L), axis=0)

ro = 1.5385
ri = 0.5385

L = ro - ri
l = (L*np.sum(averageL * range(1, len(averageL)+1))) / (np.pi * np.sum(averageL))
print('The length-scale is: {}'.format(l))
