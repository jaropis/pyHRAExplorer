import unittest
import os
from project.project_class import Project
from glob import glob
from signal_properties.RRclasses import Signal
import numpy as np

test_project = Project(path=os.getcwd()+"/project/tests/test_files/", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=1)
test_project.set_Poincare()
#test_project.set_runs(runs_shares = True)
test_project.set_spectrum(type = 'Welch')
#test_project.set_spectrum(type = 'Welch')
#test_project.set_quality()

test_project.step_through_project_files()

#y = test_project.dump_Poincare()
#y = test_project.dump_pnn(max_pnn_pro = 20, add_dec_acc = True)
#print(len(y[1]))
#y = test_project.dump_runs()
#y = test_project.dump_spectrum(ulf = False)
#print(y.get_bands(ulf = False))
# print(y.values())
#y = test_project.dump_quality()
#spectrum = test_project.project_results[1][1]['spectrum']
#bands=[0, 0.003, 0.04, 0.15, 0.4]
#ls_spec = spectrum.spectral_values(cuts=bands).values()
test_project.dump_all()
#print(y)
'''
path=os.getcwd()+"/project/tests/test_files"
file_extension=".rea"
#lister = glob(path+'/*'+file_extension)

#print([item.split("/")[-1] for item in glob(path+'/*'+file_extension)])

test_project.get_files_list()
files = [item.split("\\")[-1] for item in glob(path+'/*'+file_extension)]
local_files_list = [item.split("\\")[-1] for item in test_project.files_list]
print(glob(path+'/*'+file_extension))
print(files)
print(local_files_list)

test_project.step_through_project_files()


column_signal=1
column_annot=2
column_sample_to_sample=1
path=os.getcwd()+"/project/tests/test_files"
temp_path = path + "/" + test_project.files_list[0]
temp_signal = Signal(path_to_file=temp_path, column_annot=column_annot, column_signal=column_signal, column_sample_to_sample=column_sample_to_sample)
#temp_signal.set_poincare()
#print(temp_signal.poincare.SDNN)

bad_beats = np.where(temp_signal.annotation != 0)[0]
filtered_timetrack = np.delete(temp_signal.timetrack, bad_beats)
'''

y = 'file_name\t123\t123\n'
x = '123.rea\t123\t123\n'
#print(repr(y.strip('file_name\t \n')))
#print(repr(x[x.find('\t')+1:x.find('\n')]))

#print(test_project.files_list, test_project.project_results)
for name in ['pnn']:
            x = f'self.dump_'+name+'()'
            print(x)