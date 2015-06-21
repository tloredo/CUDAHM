import numpy as np
from matplotlib.pyplot import *

execfile("rc_settings.py")
rc('font', size=20)  # default for labels (not axis labels)

performance_iter_vs_time_data_1000=np.loadtxt('performance_iter_vs_time_data_1000.dat',delimiter=' ',usecols=(0,1))
performance_iter_vs_time_data_10000=np.loadtxt('performance_iter_vs_time_data_10000.dat',delimiter=' ',usecols=(0,1))
performance_iter_vs_time_data_100000=np.loadtxt('performance_iter_vs_time_data_100000.dat',delimiter=' ',usecols=(0,1))
performance_iter_vs_time_data_300000=np.loadtxt('performance_iter_vs_time_data_300000.dat',delimiter=' ',usecols=(0,1))
performance_iter_vs_time_data_600000=np.loadtxt('performance_iter_vs_time_data_600000.dat',delimiter=' ',usecols=(0,1))
performance_iter_vs_time_data_1000000=np.loadtxt('performance_iter_vs_time_data_1000000.dat',delimiter=' ',usecols=(0,1))

fig = figure()

ax = fig.add_subplot(1,1,1, xlim=[0, 2020000], ylim=[0, 170]) # one row, one column, first plot
ax.scatter(performance_iter_vs_time_data_1000[:,0], performance_iter_vs_time_data_1000[:,1], color ='b', marker = "o", s = 15, label = '1000 obj')
ax.plot(performance_iter_vs_time_data_1000[:,0], performance_iter_vs_time_data_1000[:,1], 'b-')
ax.scatter(performance_iter_vs_time_data_10000[:,0], performance_iter_vs_time_data_10000[:,1], color ='m', marker = "o", s = 15, label = '10000 obj')
ax.plot(performance_iter_vs_time_data_10000[:,0], performance_iter_vs_time_data_10000[:,1], 'm-')
ax.scatter(performance_iter_vs_time_data_100000[:,0], performance_iter_vs_time_data_100000[:,1], color ='y', marker = "o", s = 15, label = '100000 obj')
ax.plot(performance_iter_vs_time_data_100000[:,0], performance_iter_vs_time_data_100000[:,1], 'y-')
ax.scatter(performance_iter_vs_time_data_300000[:,0], performance_iter_vs_time_data_300000[:,1], color ='r', marker = "o", s = 15, label = '300000 obj')
ax.plot(performance_iter_vs_time_data_300000[:,0], performance_iter_vs_time_data_300000[:,1], 'r-')
ax.scatter(performance_iter_vs_time_data_600000[:,0], performance_iter_vs_time_data_600000[:,1], color ='g', marker = "o", s = 15, label = '600000 obj')
ax.plot(performance_iter_vs_time_data_600000[:,0], performance_iter_vs_time_data_600000[:,1], 'g-')
ax.scatter(performance_iter_vs_time_data_1000000[:,0], performance_iter_vs_time_data_1000000[:,1], color ='c', marker = "o", s = 15, label = '1000000 obj')
ax.plot(performance_iter_vs_time_data_1000000[:,0], performance_iter_vs_time_data_1000000[:,1], 'c-')


ax.set_xlabel('Iteration numbers')
ax.set_ylabel('Elapsed time (min)')
ax.legend(loc=2)

savefig('performance_iter_vs_time.pdf', format='pdf')

performance_obj_vs_time_data_10000=np.loadtxt('performance_obj_vs_time_data_10000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_20000=np.loadtxt('performance_obj_vs_time_data_20000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_50000=np.loadtxt('performance_obj_vs_time_data_50000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_100000=np.loadtxt('performance_obj_vs_time_data_100000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_200000=np.loadtxt('performance_obj_vs_time_data_200000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_500000=np.loadtxt('performance_obj_vs_time_data_500000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_1000000=np.loadtxt('performance_obj_vs_time_data_1000000.dat',delimiter=' ',usecols=(0,1))
performance_obj_vs_time_data_2000000=np.loadtxt('performance_obj_vs_time_data_2000000.dat',delimiter=' ',usecols=(0,1))

fig = figure()

ax = fig.add_subplot(1,1,1, xlim=[0, 1010000], ylim=[0, 170]) # one row, one column, first plot

ax.scatter(performance_obj_vs_time_data_10000[:,0], performance_obj_vs_time_data_10000[:,1], color = 'b', marker = "o", s = 15, label = '10000 iter')
ax.plot(performance_obj_vs_time_data_10000[:,0], performance_obj_vs_time_data_10000[:,1], 'b-')
ax.scatter(performance_obj_vs_time_data_20000[:,0], performance_obj_vs_time_data_20000[:,1], color = 'g', marker = "o", s = 15, label = '20000 iter')
ax.plot(performance_obj_vs_time_data_20000[:,0], performance_obj_vs_time_data_20000[:,1], 'g-')
ax.scatter(performance_obj_vs_time_data_50000[:,0], performance_obj_vs_time_data_50000[:,1], color = 'r', marker = "o", s = 15, label = '50000 iter')
ax.plot(performance_obj_vs_time_data_50000[:,0], performance_obj_vs_time_data_50000[:,1], 'r-')
ax.scatter(performance_obj_vs_time_data_100000[:,0], performance_obj_vs_time_data_100000[:,1], color = 'c', marker = "o", s = 15, label = '100000 iter')
ax.plot(performance_obj_vs_time_data_100000[:,0], performance_obj_vs_time_data_100000[:,1], 'c-')
ax.scatter(performance_obj_vs_time_data_200000[:,0], performance_obj_vs_time_data_200000[:,1], color = 'm', marker = "o", s = 15, label = '200000 iter')
ax.plot(performance_obj_vs_time_data_200000[:,0], performance_obj_vs_time_data_200000[:,1], 'm-')
ax.scatter(performance_obj_vs_time_data_500000[:,0], performance_obj_vs_time_data_500000[:,1], color = 'y', marker = "o", s = 15, label = '500000 iter')
ax.plot(performance_obj_vs_time_data_500000[:,0], performance_obj_vs_time_data_500000[:,1], 'y-')
ax.scatter(performance_obj_vs_time_data_1000000[:,0], performance_obj_vs_time_data_1000000[:,1], color = 'k', marker = "o", s = 15, label = '1000000 iter')
ax.plot(performance_obj_vs_time_data_1000000[:,0], performance_obj_vs_time_data_1000000[:,1], 'k-')
ax.scatter(performance_obj_vs_time_data_2000000[:,0], performance_obj_vs_time_data_2000000[:,1], color = 'b', marker = "o", s = 15, label = '2000000 iter')
ax.plot(performance_obj_vs_time_data_2000000[:,0], performance_obj_vs_time_data_2000000[:,1], 'b-')

ax.set_xlabel('Object numbers')
ax.set_ylabel('Elapsed time (min)')
ax.legend(loc=0)

savefig('performance_obj_vs_time.pdf', format='pdf')