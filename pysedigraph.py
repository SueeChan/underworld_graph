import matplotlib.pyplot as plt
import numpy as np
import csv

year = list(np.arange(0,3,0.05))
y_pos = np.arange(len(year))
num_env = 7
total_year = 300 +1
data = [[0.0] * total_year for i in range(num_env)]


#data = [[i * j for j in range(year)] for i in range(num_env)]
with open("thickness0.csv", mode = 'r')as file:
    reader = csv.DictReader(file)
    ct = 0
    for row in reader:
        if ct == 0:
            ct += 1
            continue

        if int(row["layer ID"]) > 300:
            break

        rela_elevat = float(row["relative elevation"])
        thickness = float(row["thickness"])

        if(rela_elevat>5):
            data[0][int(row["layer ID"])] += thickness
        elif(rela_elevat<5 and rela_elevat>=0):
            data[1][int(row["layer ID"])] += thickness
        elif(rela_elevat<0 and  rela_elevat>=-10):
            data[2][int(row["layer ID"])] += thickness
        elif(rela_elevat<-10 and  rela_elevat>=-25):
            data[3][int(row["layer ID"])] += thickness
        elif(rela_elevat<-25 and  rela_elevat>=-100):
            data[4][int(row["layer ID"])] += thickness
        elif(rela_elevat<-100 and  rela_elevat>=-200):
            data[5][int(row["layer ID"])] += thickness
        elif(rela_elevat < -200):
            data[6][int(row["layer ID"])] += thickness

        ct += 1

out = [[0.0] * len(year) for i in range(num_env)]
for i in range(num_env):
    ts = 1
    for j in range(len(year)):
        out[i][j] = data[i][ts] + data[i][ts+1] + data[i][ts+2]+ data[i][ts+3] + data[i][ts+4]
        ts += 5



env1 = np.array(out[0])
env2 = np.array(out[1])
env3 = np.array(out[2])
env4 = np.array(out[3])
env5 = np.array(out[4])
env6 = np.array(out[5])
env7 = np.array(out[6])


#plt.bar(y_pos, thickness)
p1 = plt.bar(y_pos, env1, color='darkgreen')
p2 = plt.bar(y_pos, env2, color='lawngreen', bottom=env1)
p3 = plt.bar(y_pos, env3, color='red', bottom =env1+env2)
p4 = plt.bar(y_pos, env4, color='yellow', bottom =env1+env2+env3)
p5 = plt.bar(y_pos, env5, color='DeepSkyBlue', bottom =env1+env2+env3+env4)
p6 = plt.bar(y_pos, env6, color='blue', bottom =env1+env2+env3+env4+env5)
p7 = plt.bar(y_pos, env7, color='navy', bottom =env1+env2+env3+env4+env5+env6)
#plt.xticks(y_pos, year)

plt.xticks(np.arange(0,60+2,2),list(np.arange(0,3.1,0.1)))


#plt.yticks(np.arange(0, 81, 10))
plt.ylabel('Thickness (meters)')
plt.xlabel('Time (million year)')
plt.title("Sedimentation through time along rift B - B'")
plt.legend((p1[0], p2[0], p3[0],p4[0],p5[0],p6[0],p7[0]), ("Continental facies (>5m)","Coastal plain (5 -- 0m)", "Shoreface (0 -- -10m)", "Shoreface-offshore transition (-11 -- -25m)", "Intermediate offshore (-26 -- -100m)","Distal offshore (-101 -- -200m)","Abyssal plain (<-200m)"), loc='upper center', title = 'Paleo-depth (meters)')



plt.show()
