import matplotlib.pyplot as plt
# make sure that signal.set_poincare() is run in the same file
# Currently there are three different grpahs that can be returned:
# 1. Poincare plot comapring RRn vs RRn+1 with an identity line
# 2. Histogram showing the distribution of values of RRn , together with meanRR +/- sdnn
# 3. Tachogram showing filtered RRn against time[min] with meanRR +/- sdnn shown

# WORK IN PROGRESS SOME PLOTS ARE MISSING LEGENDS/AXIS NAMES

class PlotRR:
    def __init__(self, signal):
       self.PPLOT =  self.pplot(signal)
       self.RR_HISTOGRAM = self.rr_histogram(signal)
       self.TACHOGRAM = self.tachogram(signal)

    def pplot(self, signal, color = 'darkblue'):
        #print('test', signal.poincare.meanRR)
        global_min = min([min(signal.poincare.xii[1:]), min(signal.poincare.xi[1:])])
        #print(rr.poincare.xi)

        #RRplot = plt.subplot(3,2,(1,4))
        #RRplot = plt.subplot(2,1,1)
        p_plot = plt.figure()
        plt.scatter(x = signal.poincare.xi[1:], y = signal.poincare.xii[1:],  facecolors='none', edgecolors= color, s = 30, alpha = 0.5)
        plt.axline((global_min-50,global_min-50), slope=1,c = 'black', ls = '--')
        plt.xlabel('Rnn')
        plt.ylabel('RRn+1')
        #plt.set(adjustable='box', aspect='equal')
        plt.axis('square')
        plt.show()
        #return p_plot
    
    def rr_histogram(self, signal):
        hist = plt.figure()
        plt.hist(signal.poincare.xi[1:], bins = 25, edgecolor = 'darkblue')
        plt.axvline(x = signal.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 2)
        plt.axvline(x = signal.poincare.meanRR + signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
        plt.axvline(x = signal.poincare.meanRR - signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
        plt.ylabel('Count')
        plt.xlabel('Rnn')

        return hist
    
    def tachogram(self, signal):
        tacho = plt.figure()
        plt.plot(signal.poincare.filtered_time, signal.poincare.xii, color='black', linestyle='--', linewidth=0.3)
        plt.scatter(x = signal.poincare.filtered_time, y = signal.poincare.xii,  facecolors='none', edgecolors= 'black', alpha = 0.75, s = 5, linewidths = 0.5)
        plt.axhline(y = signal.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 1)
        plt.axhline(y = signal.poincare.meanRR + signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
        plt.axhline(y = signal.poincare.meanRR - signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
        plt.ylabel('RR')
        plt.xlabel('Time [min]')

        return tacho

    #def all (return all plots as one figure? not sure how useful)






