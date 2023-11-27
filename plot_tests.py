from signal_properties.RRclasses import Signal
import numpy
import matplotlib.pyplot as plt
import scipy.signal as sc
# PLACE FOR TESTS - WILL BE REMOVED 

rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/0582a.rea", 1, 2, 0, square_filter=(500,1500), annotation_filter=(1, 2, 3))
#rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/test_flags.txt", 1, 2, 0, square_filter=(500,1500), annotation_filter=(1, 2, 3))
rr.set_poincare()
rr.set_LS_spectrum()
rr.set_Welch_spectrum()
#rr.set_runs()
#rr.set_plots()
#print(rr.poincare.pNN50, rr.poincare.pnnx(), rr.poincare.pnnx(100))
#14.316820903647251 14.316820903647251 0.43549265106151336

#print(rr.poincare.pnnx()[1], rr.poincare.pnn_pro(x = 10), rr.poincare.pNN50)
#print(rr.Welch_spectrum.resampled_rr, rr.Welch_spectrum.resampled_timetrack, rr.Welch_spectrum.interpolated_rr)
#print(type(rr.Welch_spectrum.welch_spectrum))

x = rr.Welch_spectrum.welch_bands
xx = rr.Welch_spectrum.welch_bands_24h

#print(rr.Welch_spectrum.welch_bands_ulf, rr.Welch_spectrum.welch_bands_vlf, rr.Welch_spectrum.welch_bands_lf, rr.Welch_spectrum.welch_bands_hf, rr.Welch_spectrum.welch_bands_tp, rr.poincare.SDNN**2, rr.poincare.SDNN**2/rr.Welch_spectrum.welch_bands_tp)

#print(rr.LS_spectrum.get_bands([0.003, 0.04, 0.15, 0.4], df))
#print(rr.LS_spectrum.get_bands([0.04, 0.15, 0.4], df))
#print(rr.Welch_spectrum.test_resample)
#total_power = sum(rr.LS_spectrum.periodogram) * ((rr.LS_spectrum.frequency[1] -  rr.LS_spectrum.frequency[0]))
#total_power2 = sum(rr.LS_spectrum.periodogram) * (rr.LS_spectrum.frequency[1] -  rr.LS_spectrum.frequency[0])                                            
#print(total_power, total_power2)
#print(rr.LS_spectrum.build_spectrum())

'''print(rr.LS_spectrum.periodogram, rr.LS_spectrum.frequency)
bands = rr.LS_spectrum.get_bands(cuts=[0, 0.25, 0.94, 2.5], df=rr.LS_spectrum.frequency[1]-rr.LS_spectrum.frequency[0])
bands2 = rr.LS_spectrum.get_bands(cuts=[0, 0.04, 0.15, 0.4], df=rr.LS_spectrum.frequency[1]-rr.LS_spectrum.frequency[0])
total_power2 = sum(rr.LS_spectrum.periodogram) * (rr.LS_spectrum.frequency[1] -  rr.LS_spectrum.frequency[0])                                            
print('power:', total_power2, sum(rr.LS_spectrum.periodogram), sum(bands), sum(bands2))
#rr.LS_spectrum.plot_periodogram()
#plt.show()
'''
#bands = rr.LS_spectrum.get_bands(cuts=[0, 0.25, 0.94, 2.5], df=rr.LS_spectrum.frequency[1]-rr.LS_spectrum.frequency[0])
#print(rr.LS_spectrum.periodogram, rr.LS_spectrum.frequency)

#bands = rr.LS_spectrum.get_spectral_bands(cuts = [0, 0.04, 0.15, 0.4])
#print(bands, sum(bands))

'''
print(rr.LS_spectrum.spectral_values(), 'variance', numpy.var(rr.LS_spectrum.filtered_signal))

print(rr.LS_spectrum.spectral_bands, rr.LS_spectrum.spectral_bands_24h)
'''


#rr.LS_spectrum.spectrum.plot_spectrum(mode = 'Rad')
#plt.show()


#print(rr.LS_spectrum.spectrum.spectral_bands, rr.Welch_spectrum.spectrum.spectral_bands)
#print(rr.LS_spectrum.spectrum.LF_HF_ratio)
#rr.LS_spectrum.spectrum.plot_spectrum(mode = 'Hz', ulf = False, color_bands= False)
#print(rr.LS_spectrum.spectrum.frequency_hz)
#print(case)
#plt.show()
start_x = 0
stop_x = 30
step = 10
for x in range(start_x,stop_x+step,step):
    print(str(x) + "-" + str(x+step) , rr.poincare.pnn_range(x1 = x, x2 = x+step))

pro_start = 0
pro_end = 20
step = 1
for x in range(pro_start,pro_end+step,step):
    print(str(x) + "-" + str(x+step) + "%", rr.poincare.pnn_range_pro(x1 = x, x2 = x+step))