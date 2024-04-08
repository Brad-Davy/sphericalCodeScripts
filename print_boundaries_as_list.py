


with open('thermal_bl_thickness_ave.dat', 'r') as file:
    r = []
    Trms = []
    for lines in file.read().split('\n'):
        lineData = lines.split('  ')
        if len(lineData) == 3:
            r.append(float(lineData[1]))
            Trms.append(float(lineData[2]))

print('r: \n')
print(r)
print('\n')
print('Trms: \n')
print(Trms)
print('\n')

with open('vel_bl_s_ave.dat', 'r') as file:
    Uh = []
    for lines in file.read().split('\n'):
        lineData = lines.split()
        if len(lineData) == 7:
            try:
                Uh.append(float(lineData[6]))
            except:
                pass


print('Uh: \n')
print(Uh)
