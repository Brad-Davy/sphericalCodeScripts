
files = ['mAverage.txt', 'lAverage.txt', 'mSTD.txt', 'lSTD.txt']

def convertToArray(textFile):
    arr = []
    contentsOfTxtFile = open('img/{}'.format(textFile), 'r').read()

    scrubbedTxtFile = contentsOfTxtFile.replace('[','')
    scrubbedTxtFile = scrubbedTxtFile.replace(']','')

    for lines in scrubbedTxtFile.split('\n'):
        for number in lines.split(' '):
            try:
                arr.append(float(number))
            except:
                pass
    return arr

for file in files:
    print('-'*60)
    print(file)
    print('-'*60)
    print(convertToArray(file))
