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
        '''
        This function uses xi and xii created by the prepare_PP function (in Poincare.py) to build a Poincare plot.
        In the Poncare plot, Rnn (xi) is plotted against Rnn+1 (xii). Alongside the the points, the plot also includes
        a dashed identity line (x = y).
        The function accepts color (string) and size (int) parameters to change the colour and size of the points
        on the Poincare plot respectively. 
        '''
        global_min = min([min(signal.poincare.xii[1:]), min(signal.poincare.xi[1:])])
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
        '''
        This function uses xi created from prepare_PP function to plot the distribution of RR signals as a histogram.
        Alongside the histogram, mean and mean +/- sd are shown as red and green lines respectively.
        Functions accepts parameters color, edgecolor and binds that modify the color of the bins, their edges and their 
        number. 
        '''
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
        '''
        Function that uses the xii and filtered_time to create a tachogram, ploting RRsignal against time. 
        Together with the tachogram, the mean and mean +/- sd of the RR signal are also displayed as red and green 
        dashed lines respectively.
        Alongside signal, the function also excepts markersize, linewidth and color parameters that control the size,
        edge thickness and colour of the ploted points. 
        '''
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






