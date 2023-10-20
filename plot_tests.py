from signal_properties.RRclasses import Signal
import numpy
import matplotlib.pyplot as plt
import scipy.signal as sc
# PLACE FOR TESTS - WILL BE REMOVED 

#rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/0582a.rea", 1, 2, 0, square_filter=(500,1500), annotation_filter=(1, 2, 3))
rr = Signal("C:/Users/k52672mg/OneDrive - The University of Manchester/Analysis/PIPS_HRAEXPLORER/test_files/test_flags.txt", 1, 2, 0, square_filter=(500,1500), annotation_filter=(1, 2, 3))
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
print(rr.Welch_spectrum.welch_bands)
#print(rr.Welch_spectrum.test_resample)