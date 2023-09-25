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

    def pplot(self, signal, color = 'darkblue', size = 30):
        #print('test', signal.poincare.meanRR)
        global_min = min([min(signal.poincare.xii[1:]), min(signal.poincare.xi[1:])])
        #print(rr.poincare.xi)

        #RRplot = plt.subplot(3,2,(1,4))
        #RRplot = plt.subplot(2,1,1)
        p_plot = plt.figure()
        plt.scatter(x = signal.poincare.xi[1:], y = signal.poincare.xii[1:],  facecolors='none', edgecolors= color, s = size, alpha = 0.5)
        plt.axline((global_min-50,global_min-50), slope=1,c = 'black', ls = '--')
        plt.xlabel('Rnn')
        plt.ylabel('RRn+1')
        #plt.set(adjustable='box', aspect='equal')
        plt.axis('square')
        #plt.show()
        return p_plot
    
    def rr_histogram(self, signal, color = 'blue', edgecolor = 'darkblue', bins = 25):
        hist = plt.figure()
        plt.hist(signal.poincare.xi[1:], bins = bins, edgecolor = edgecolor, color = color)
        plt.axvline(x = signal.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 2)
        plt.axvline(x = signal.poincare.meanRR + signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
        plt.axvline(x = signal.poincare.meanRR - signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1.5)
        plt.ylabel('Count')
        plt.xlabel('Rnn')
        #plt.show()
        return hist
    
    def tachogram(self, signal, markersize = 5, linewidth = 0.3, color = 'black'):
        tacho = plt.figure()
        plt.plot(signal.poincare.filtered_time, signal.poincare.xii, color=color, linestyle='--', linewidth=linewidth)
        plt.scatter(x = signal.poincare.filtered_time, y = signal.poincare.xii,  facecolors='none', edgecolors= color, alpha = 0.75, s = markersize, linewidths = 0.5)
        plt.axhline(y = signal.poincare.meanRR, linestyle = 'dashed', color = 'red', linewidth = 1)
        plt.axhline(y = signal.poincare.meanRR + signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
        plt.axhline(y = signal.poincare.meanRR - signal.poincare.SDNN, linestyle = 'dashed', color = 'lightgreen', linewidth = 1)
        plt.ylabel('RR')
        plt.xlabel('Time [min]')
        #plt.show()

        return tacho

    #def all (return all plots as one figure? not sure how useful)






