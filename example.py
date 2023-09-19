# this is an example of using the HRA explorer with the AVA files
# you need to put this file (example.py) on the same level as the folder signal_classes, or use relative imports in the
# line below
from signal_properties.RRclasses import Signal
from numpy import sqrt
# the rr object of the Signal class is created using the following arguments:
# - the path to the file (obviously, below you can see my own path - you will have to use your own paths)
# - 0 is the (Python) number of the signal (RR intervals) column
# - 1 is the (Python) number of the annotation column
# - annotation_filter = (1, 2, 3) means: filter out ventricular beats (1), supraventricular beats (2) and artifacts (3)
# (this is the standard coding of non-sinus beats)
#rr = Signal("/Users/jaropis/Dropbox/AVA_Results/RR_intervals/AVA02_2017-01-18.txt", 0, 1, annotation_filter=(1, 2, 3))
rr = Signal("./RR1.csv", 0, 1, annotation_filter=(1, 2, 3))
rr.set_poincare() # here the time domain HRV parameters are calculated
# and now let's see some of the results
hrv = {"SDNN": rr.poincare.SDNN, "RMSSD": rr.poincare.SD1*sqrt(2), "SD1": rr.poincare.SD1, "SD2": rr.poincare.SD2}
print('SDNN={SDNN}, RMSSD={RMSSD}, SD1={SD1}, SD2={SD2}'.format(**hrv))
