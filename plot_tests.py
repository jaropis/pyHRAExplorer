from signal_properties.RRclasses import Signal
import matplotlib.pyplot as plt
# Created to test the new plot function

# PLACE TO TEST PLOTS WILL BE REMOVED (code moved to the plotRR.py)

rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/0582a.rea", 1, 2, 0, annotation_filter=(1, 2, 3))
rr.set_poincare()
global_min = min([min(rr.poincare.xii[1:]), min(rr.poincare.xi[1:])])
#print(rr.poincare.xi)

#fig, (RRplot, RRhist) = plt.subplots(nrows=2, sharex= True, subplot_kw=dict(frameon=False))
#RRplot = plt.subplot(3,2,(1,4))
#RRplot = plt.subplot(2,1,1)
#RRplot.scatter(x = rr.poincare.xi[1:], y = rr.poincare.xii[1:],  facecolors='none', edgecolors= 'darkblue', s = 30, alpha = 0.5)
#RRplot.axline((global_min-50,global_min-50), slope=1,c = 'black', ls = '--')
#RRplot.set_xlabel('Rnn')
#RRplot.set_ylabel('RRn+1')
#RRplot.set(adjustable='box', aspect='equal')
#RRplot.axis('square')
#print(rr.poincare.xii[1:])
#print(rr.poincare.xi[1:])
#print(rr.poincare.filtered_time[1:])
#RRhist = plt.subplot(3,2,(5,6))
#RRhist = plt.subplot(2,1,2)
#RRhist.hist(rr.poincare.xi[1:], bins = 25, edgecolor = 'darkblue')
#RRhist.axvline(x = rr.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 2)
#RRhist.axvline(x = rr.poincare.meanRR + rr.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
#RRhist.axvline(x = rr.poincare.meanRR - rr.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
#RRhist.set_ylabel('Count')
#RRhist.set_xlabel('Rnn')

#print(len(rr.timetrack), len(rr.signal), len(rr.poincare.xii))
#print(where(rr.annotation == 0)[0])
#print(rr.timetrack)
#print(rr.poincare.xi, rr.poincare.xii, rr.poincare.filtered_time)

#plt.plot(rr.poincare.filtered_time, rr.poincare.xii, color='black', linestyle='--', linewidth=0.3)
#plt.scatter(x = rr.poincare.filtered_time, y = rr.poincare.xii,  facecolors='none', edgecolors= 'black', s = 10)
#plt.axhline(y = rr.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 1)
#plt.axhline(y = rr.poincare.meanRR + rr.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
#plt.axhline(y = rr.poincare.meanRR - rr.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
#plt.show()


#print('meanRR:', rr.poincare.meanRR)
#print('CV:', rr.poincare.CV)
#plt.show()
#rr.plotRR.PPplot

#print(rr.annotation)


print(type(rr.poincare.HRA1), rr.poincare.HRA2, rr.poincare.HRAT, rr.poincare.pNN50, rr.poincare.ND)
