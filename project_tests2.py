import unittest
import os
from project.project_class import Project
from glob import glob
from signal_properties.RRclasses import Signal
import numpy as np

test_project = Project(path=os.getcwd()+"/project/tests/test_files/", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=1)
#test_project = Project(path=os.getcwd()+"/project/tests/test_files3/", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=6)
test_project.set_filters(annotation_filter = (1,2,3), square_filter=(500,1500))
#test_project.set_Poincare()
#test_project.set_pnn()
#test_project.set_pnn_range()
#test_project.set_runs()
#test_project.set_spectrum(spectrum_type= 'Welch')
test_project.set_spectrum()
#test_project.set_quality()

test_project.step_through_project_files()

#y = test_project.dump_Poincare()
#y = test_project.dump_pnn(max_pnn_pro = 20, add_dec_acc = True)
#print(len(y[1]))
#y = test_project.dump_runs()
#y = test_project.dump_spectrum(ulf = False)
#print(y.get_bands(ulf = False))
# print(y.values())
#y = test_project.dump_quality(dump = False)
#spectrum = test_project.project_results[1][1]['spectrum']
#bands=[0, 0.003, 0.04, 0.15, 0.4]
#ls_spec = spectrum.spectral_values(cuts=bands).values()
#test_project.dump_all(max_pnn_pro=20, add_dec_acc=False)
#test_project.dump_pNN_range(end = 200, add_dec_acc=True, dump = True)
#test_project.dump_pNN_range_pro(end = 20, add_dec_acc=True, dump = True)
#poincare = test_project.project_results[0][1]['Poincare']
#print(poincare.SDNN)
#print(y[1][0])
#test_project.write_state()
test_project.dump_all(ulf=False)
