from signal_properties.RRclasses import Signal
import matplotlib.pyplot as plt
# Created to test the new plot function

rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/0582a.rea", 1, 2, 0, annotation_filter=(1, 2, 3))
rr.set_poincare()
rr.set_plots()

# functions (work in progress, the input function is for easy testing):

'''
x = input('Choose plot: 1. PP plot 2. Histogram 3. Tachogram ')
if x == '1':
    rr.plotRR.PPLOT
elif x == '2':
     rr.plotRR.RR_HISTOGRAM
elif x == '3':
    rr.plotRR.TACHOGRAM

'''
#rr.plotRR.PPLOT
# might create a separate function to read directly from file ?
#PPLOT default : color = 'darkblue', size = 30
rr.plotRR.pplot(rr, color = 'green', size = 20)

# rr_histogram default: color = 'blue', edgecolor = 'darkblue', bins = 25
rr.plotRR.rr_histogram(rr, color = 'pink', edgecolor = 'red', bins = 10)

# tachogram default: markersize = 5, linewidth = 0.3, color = 'black'z
rr.plotRR.tachogram(rr, color = 'red', markersize = 10, linewidth = 0.5)

plt.show()