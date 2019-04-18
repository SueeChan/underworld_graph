import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

#############################
#    input values           #
#############################
#TODO: change the values to desired input

last_timesteps = 300 #make sure it is divisible by (bar_interval/checkpoint_interval)
checkpoint_interval = 0.01 #in megayears
bar_interval = 0.05 #megayears per bar
num_env = 7
path = ""  #location of the directory 
file_name = path + "figuresue300.csv"  #csv file to read from
x_axis_label = 'Time (million year)'
y_axis_label = 'Thickness (meters)'
title = "Sedimentation through time along rift B - B'"
legend = ("Continental facies (>5m)",
          "Coastal plain (5 -- 0m)",
          "Shoreface (0 -- -10m)",
          "Shoreface-offshore transition (-11 -- -25m)",
          "Intermediate offshore (-26 -- -100m)",
          "Distal offshore (-101 -- -200m)",
          "Abyssal plain (<-200m)")
bar_per_xlabel = 2
list_of_colour = ['darkgreen', 'lawngreen', 'red', 'yellow','DeepSkyBlue', 'blue', 'navy']


# define the upper bound and lower bound of depositional env. by relative elevations in meter
# format:  (<upper bound>, <lower bound>)
#        - if there aren't a boundary write None
#        - [lower bound, upper bound) i.e. exclusive upper bound, inclusive lower bound
# order: descending order of depositional env.'s relative elevelation
list_of_depoEnv_definition = [(None, 5), (5, 0), (0, -10), (-10, -25), (-25, -100), (-100, -200), (-200, None)]



#####################################################################
#                     input file format                             #
#   - chaning space delimited input file to comma delimited file    #
#####################################################################
#TODO: uncomment if needed


# column_name = '"thickness","layer ID","relative elevation","Points:0","Points:1","Points:2"'
# cter = 0
# newfile = file_name + '_comma_delimited.csv'
# with open(file_name) as infile, open(newfile, 'w') as outfile:
#     for line in infile:
#         if(cter == 0):
#             outfile.write(column_name)
#             outfile.write("\n")
#         else:
#             outfile.write(" ".join(line.split()).replace(' ', ','))
#             outfile.write("\n")
#
#
#         cter += 1
# file_name = newfile


####################################################
#        dgathering info and plotting              #
####################################################

last_magayears = last_timesteps*checkpoint_interval

if(last_timesteps%(bar_interval/checkpoint_interval) != 0):
    print(" ")
    print('+======== !!! ATENTION !!! =========+')
    print('Last timesteps ' + str(last_timesteps) + ' cannot be completely divided by bar interval')
    print('+===================================+')
    print(" ")
    raise Exception("Last timesteps is not divisible by bar interval")


number_of_bars = (last_magayears/bar_interval)
label_every_megayear = last_magayears/ (number_of_bars/ bar_per_xlabel)
total_ts = last_timesteps +1

list_of_megayear = list(np.arange(0,last_magayears,bar_interval))
y_pos = np.arange(len(list_of_megayear))


list_of_envbar = []
env_bar_legend = []
#a 2-D array storing the environment and the thickness of each environment
data = [[0.0] * total_ts for i in range(num_env)]


####################################################
#              declare variables                   #
####################################################
with open(file_name, mode = 'r')as file:
    reader = csv.DictReader(file)
    ct = 0

    for row in reader:
        count  = 0
        if ct == 0:
            ct += 1
            continue

        if float(row["layer ID"]) > last_timesteps:
            break

        rela_elevat = float(row["relative elevation"])
        thickness = float(row["thickness"])



        for (x, y) in list_of_depoEnv_definition:
            if(x is None):
                if(rela_elevat>= y):
                    data[count][int(float(row["layer ID"]))] += thickness
                    break
            elif(y is None):
                if(rela_elevat < x):
                    data[count][int(float(row["layer ID"]))] += thickness
                    break
            else:
                if(rela_elevat<x and rela_elevat>=y):
                    data[count][int(float(row["layer ID"]))] += thickness
                    break
            count += 1
        ct += 1



out = [[0.0] * len(list_of_megayear) for i in range(num_env)]

for i in range(num_env):
    #from first time step, we ignore the timestep 0
    ts = 1
    for j in range(len(list_of_megayear)):
        out[i][j] = data[i][ts] + data[i][ts+1] + data[i][ts+2]+ data[i][ts+3] + data[i][ts+4]
        ts += 5



for i in range(num_env):
    if(i == 0):
        list_of_envbar.append(plt.bar(y_pos, np.array(out[i]), color=list_of_colour[i]))
        data_of_envbar = np.array(out[i])
    else:
        list_of_envbar.append(plt.bar(y_pos, np.array(out[i]), color=list_of_colour[i], bottom=data_of_envbar))
        data_of_envbar = data_of_envbar + np.array(out[i])

    env_bar_legend.append(list_of_envbar[i][0])


plt.xticks(np.arange(0,number_of_bars+bar_per_xlabel, bar_per_xlabel),list(np.arange(0,last_magayears + label_every_megayear,label_every_megayear)))

plt.ylabel(y_axis_label)
plt.xlabel(x_axis_label)
plt.title(title)
plt.legend(tuple(env_bar_legend), legend, loc='upper center', title = 'Paleo-depth (meters)')

fig = plt.gcf()
plt.show()
fig.set_size_inches(18.5, 10.5)
fig.savefig(path+'sedigraph.png', dpi=100)
