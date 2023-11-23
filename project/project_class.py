from glob import glob
from signal_properties.RRclasses import  Signal

class Project:
    """
    This class separates the data from the GUI and from the mathematics. It operates on the mathematics and communicates
    with the GUI.
    The main method of the Class is the step_thorugh_project class which goes over all the files in a project (folder
    with files), and calculates the HRV/HRA properties of the files
    """
    def __init__(self, path, file_extension, column_signal, column_annot, column_sample_to_sample):
        self.project_name = None
        self.path = path
        self.file_extension = file_extension
        self.column_signal = column_signal
        self.column_annot = column_annot
        self.column_sample_to_sample = column_sample_to_sample
        self.quotient_filter = -1
        self.square_filter=(-8000, 8000)
        self.annotation_filter=()
        self.files_list = self.get_files_list()

        # these three flags say whether or not the specific method should be used
        self.Poincare_state = False
        self.pnn_state = False
        self.runs_state = False
        self.spectrum_state = False
        self.quality_state = False

        self.project_results = [] # this list of lists will hold the name of the file and the self.file_results for
        # each file eg. [[filename1, {Poincare: , runs: , LS_spectrum}], [filename2, {Poincare: , runs: , LS_spectrum}}

    def get_files_list(self):
        """
        build a list of the files associated with the project, i.e. in the correct directory, with the correct
        extension
        """
        #return [item.split("/")[-1] for item in glob(self.path+'/*'+self.file_extension)]
        return [item.split("\\")[-1] for item in glob(self.path+'/*'+self.file_extension)]

    def set_Poincare(self):
        """
        this means: calculate the Poincare descriptors
        """
        self.Poincare_state = True

    def set_pnn(self):
        """
        this means: calculate the pNN and pNN percent descriptors
        """
        self.pnn_state = True

    def set_runs(self, runs_shares = False):
        """
        this means: calculate runs
        """
        self.runs_state = True
        self.runs_shares = runs_shares

    
    def set_spectrum(self, type = 'LS'):
        """
        this means: calculate spectrum
        """
        self.spectrum_state = True
        self.spectrum_type = type
    '''
    def set_LS_spectrum(self):
        """
        this means: calculate Lomb-Scargle spectrum
        """
        self.LS_spectrum_state = True
    '''

    def set_quality(self):
        """
        this means: calculate quality parameters (number of beats if each type)
        """
        self.quality_state = True

    def set_columns(self, column_signal=None, column_annotation=None, column_sample_to_sample=None):
        """
        sets the columns in the files
        :column_signal: the number of the column holding the signal
        :column_annotation: the number of the column holdng the annotations
        :column_sample_to_sample: the number of the column holding the sample-to-sample values
        :: - does not return anything - just modifies the arguments
        """
        self.column_signal = column_signal
        self.column_annot = column_annotation
        self.column_sample_to_sample = column_sample_to_sample

    def set_filters(self, annotation_filter=(), square_filter=(-8000, 8000), quotient_filter=-1):
        """
        setting the filters
        :param annotation_filter: sets the tuple holding annotations to remove
        :param square_filter: sets the upper and lower values to cut
        :param quotient_filter: sets the quotient under/over which to remove a beat (sample)
        :return: does not return anything
        """
        self.annotation_filter = annotation_filter
        self.square_filter = square_filter
        self.quotient_filter = quotient_filter

    def step_through_project_files(self):
        """
        this is the main method of this class - it visits every file and, if the _state variable is 1 calculates
        the respective HRV/HRA method
        :return: dictionary with results, results = {Poincare: [], runs: [], LS_spectrum: []} - a list may be empty if the user
         does not want a specific type of result
        """
        temp_poincare = None
        temp_spectrum = None
        #temp_LS_spectrum = None
        temp_runs = None
        temp_quality = None
        # above: just to begin with something
        for file in self.files_list:
            temp_path = self.path + "/" + file
            temp_signal = Signal(path_to_file=temp_path, column_annot=self.column_annot, column_signal=self.column_signal,
                                 column_sample_to_sample=self.column_sample_to_sample, annotation_filter=self.annotation_filter,
                                 square_filter=self.square_filter, quotient_filter=self.quotient_filter)
            if self.Poincare_state or self.pnn_state:
                temp_signal.set_poincare()
                temp_poincare = temp_signal.poincare
            else:
                temp_poincare = None

            if self.runs_state:
                temp_signal.set_runs()
                temp_runs = temp_signal.runs
            else:
                temp_runs = None

            if self.spectrum_state and self.spectrum_type == 'LS':
                temp_signal.set_LS_spectrum()
                temp_spectrum = temp_signal.LS_spectrum
            elif self.spectrum_state and self.spectrum_type == 'Welch':
                temp_signal.set_Welch_spectrum()
                temp_spectrum = temp_signal.Welch_spectrum
            
            '''
            if self.LS_spectrum_state:
                temp_signal.set_LS_spectrum()
                temp_LS_spectrum = temp_signal.LS_spectrum
            '''

            if self.quality_state:
                temp_quality = temp_signal.quality(temp_signal.annotation)
            temp_file_results = {"Poincare": temp_poincare, "runs": temp_runs, "Spectrum": temp_spectrum, 'Quality': temp_quality}
            self.project_results.append([file, temp_file_results])

    # methods to finish
    def read_state(self):
        """
        this method checks if the project already exists, reads from the .project files the state of the project, and,
        if some of the calculations have already been performed, it prevents the Project from re-doing them
        :return:
        """
        try:
            input_file = open(self.path + "/.HRAproject", 'r')
            self.project_name = input_file.readline().split(':')[1].rstrip()
            self.files_no = int(input_file.readline().split(':')[1].rstrip())
            self.column_signal = int(input_file.readline().split(':')[1].rstrip())
            self.column_annot = int(input_file.readline().split(':')[1].rstrip())
            self.column_sample_to_sample = int(input_file.readline().split(':')[1].rstrip())
            self.annotation_filter = eval(input_file.readline().split(':')[1].rstrip())
            self.square_filter = eval(input_file.readline().split(':')[1].rstrip())
            self.quotient_filter = int(input_file.readline().split(':')[1].rstrip())
            self.Poincare_state = bool(input_file.readline().split(':')[1].rstrip())
            self.runs_state = bool(input_file.readline().split(':')[1].rstrip())
            self.LS_spectrum_state = bool(input_file.readline().split(':')[1].rstrip())
            self.quality_state = bool(input_file.readline().split(':')[1].rstrip())
            input_file.close()
            return(True)
        except Exception:
            return(False)

    def write_state(self):
        """
        this method writes the state of the project to the drive
        :return:
        """
        try:
            output_file = open(self.path + "/.HRAproject", 'w')

            output_line = "project name:" + str(self.project_name) + "\n"
            output_line += "number of files:"+ str(len(self.files_list)) + "\n"
            output_line += "column signal:" + str(self.column_signal) + "\n"
            output_line += "column annotation:" + str(self.column_annot) + "\n"
            output_line += "column sample to sample:" + str(self.column_sample_to_sample) + "\n"
            output_line += "annotation filter:" + str(self.annotation_filter) + "\n"
            output_line += "square filter:" + str(self.square_filter) + "\n"
            output_line += "quotient filter:" + str(self.quotient_filter) + "\n"
            output_line += "Poincare state:" + str(int(self.Poincare_state)) + "\n"
            output_line += "runs state:" + str(int(self.runs_state)) + "\n"
            #output_line += "LS_spectrum state:" + str(int(self.LS_spectrum_state)) + "\n"
            output_line += "Quality state:" + str(int(self.quality_state)) + "\n"
            output_file.write(output_line)
            output_file.close()
            return True
        except Exception:
            return False

    def dump_Poincare(self):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the Poincare plot descriptors for each
        file in the project
        :return:
        """
        #results_first_line = "filename\tSDNN\tSD1\tSD2\tSD1d\tSD1a\tC1d\tC1a\tSD2d\tSD2a\tC2d\tC2a\tSDNNd\tSDNNa\tCd\tCa\n"
        results_first_line = "filename\tSDNN\tSD1\tSD2\tSD2/SD1\tmeanRR\tpNN50\tSD1d\tC1d\tSD1a\tC1a\tSD1I\tND\tSD2d\tC2d\tSD2a\tC2a\tSD2I\tSDNNd\tCd\tSDNNa\tCa\tHRA1\tHRA2\tHRAT\tHRAN\tHRAcomp\tCS\tCSa\tCSd\tCLa\tCLd\n"
        results_file = self.build_name(prefix="Poincare_")
        results = open(results_file, 'w')
        results.write(results_first_line)
        all = []
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_poincare_object = file_result[1]['Poincare'] # this is a dictionary - I select key Poincare
            res_line = file_name + "\t"
            '''res_line += str(temp_poincare_object.SDNN) + "\t" + str(temp_poincare_object.SD1) + "\t" + str(temp_poincare_object.SD2) + "\t" + \
                        str(temp_poincare_object.SD1d) + "\t" + str(temp_poincare_object.SD1a) + "\t" + str(temp_poincare_object.C1d) + "\t" + \
                        str(temp_poincare_object.C1a) + "\t" + str(temp_poincare_object.SD2d) + "\t" + str(temp_poincare_object.SD2a) + "\t" + \
                        str(temp_poincare_object.C2d) + "\t" + str(temp_poincare_object.C2a) + "\t" + str(temp_poincare_object.SDNNd) + "\t" + \
                        str(temp_poincare_object.SDNNa) + "\t" + str(temp_poincare_object.Cd) + "\t" + str(temp_poincare_object.Ca) + "\n"
            '''
            res_line += str(temp_poincare_object.SDNN) + "\t" + str(temp_poincare_object.SD1) + "\t" + str(temp_poincare_object.SD2) + "\t" + \
                str(temp_poincare_object.SD2_SD1) + "\t" + str(temp_poincare_object.meanRR) + "\t" + str(temp_poincare_object.pNN50) + "\t"+ \
                    "\t".join([str(_) for _ in temp_poincare_object.short_term_asymmetry()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.long_term_asymmetry()]) + \
                    "\t" + "\t".join([str(_) for _ in temp_poincare_object.total_asymmetry()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.hra_forms()]) + \
                    "\t" + "\t".join([str(_) for _ in temp_poincare_object.short_term_variability()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.long_term_variability()]) + "\n"

            '''
            self.SD1d, self.C1d, self.SD1a, self.C1a, self.SD1I, self.ND = self.short_term_asymmetry()
        self.SD2d, self.C2d, self.SD2a, self.C2a, self.SD2I = self.long_term_asymmetry()
        self.SDNNd, self.Cd, self.SDNNa, self.Ca = self.total_asymmetry()
        self.HRA1, self.HRA2, self.HRAT, self.HRAN, self.HRAcomp = self.hra_forms()
        # HRV
            # HRV
            self.CS, self.CSa, self.CSd = self.short_term_variability()
            self.CLa, self.CLd = self.long_term_variability()
            '''
            results.write(res_line)
            all.append(res_line)
        results.close()
        return(all, self.project_results)
        
    def dump_pnn(self, max_pnn = 100, pnn_step = 10, max_pnn_pro = 10, pnn_pro_step = 0.5, add_dec_acc = False):
        max_pnn = max_pnn
        results_file = self.build_name(prefix="PNN_" if not add_dec_acc else "PNN_DEC_ACC_")
        results = open(results_file, 'w')
        results_first_line = 'filename\t' + "\t".join("pNN_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step))
        # Adding optional PNNs for dec and acc 
        results_first_line += "\t" if not add_dec_acc else "\t" + "\t".join("pNN_dec_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step)) + \
        "\t" + "\t".join("pNN_acc_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step))
        # Adding pNN%
        results_first_line += "\t" + "\t".join("pNN_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step)))
        # Adding optional pNN% for dec and acc
        results_first_line += "\n" if not add_dec_acc else "\t" + "\t".join("pNN_dec_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + \
            "\t" + "\t".join("pNN_acc_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + "\n"
        results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            res_line = file_name
            temp_poincare_object = file_result[1]['Poincare']
            res_line += "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[0]) for _ in range(0, max_pnn + pnn_step, pnn_step))
            # Optional results for dec and acc
            res_line += "\t" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[1]) for _ in range(0, max_pnn + pnn_step, pnn_step)) + \
             "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[2]) for _ in range(0, max_pnn + pnn_step, pnn_step)) + "\t"
            res_line += "\t".join(str(temp_poincare_object.pnn_pro(_/10)[0]) for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step)))
            # Optional results for dec and acc
            res_line += "\n" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnn_pro(_/10)[1]) for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + \
            "\t" + "\t".join(str(temp_poincare_object.pnn_pro(_/10)[2]) for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + "\n"
            results.write(res_line)
            all_results.append(res_line)
            #temp_poincare_object.pnnx()[0]
            #temp_poincare_object.pnn_pro()[0]
        results.close()
        return [results_first_line, all_results] 
        
    def dump_runs(self):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the monotonic runs for each
        file in the project
        :return:
        """
        max_dec_len, max_acc_len, max_neutral_len = self.find_longest_runs()
        print(max_dec_len, max_acc_len, max_neutral_len)
        results_first_line = "file_name" + "\t" + "\t".join(["dec"+str(_+1) for _ in range(max_dec_len)]) + "\t"+ \
                     "\t".join(["acc" + str(_ + 1) for _ in range(max_acc_len)]) + "\t" + \
                     "\t".join(["neutral" + str(_ + 1) for _ in range(max_neutral_len)])
        results_first_line += "\n" if not self.runs_shares else "\t" + "\t".join(["dec"+str(_+1)+"_share" for _ in range(max_dec_len)]) + "\t"+ \
                     "\t".join(["acc" + str(_ + 1) + "_share" for _ in range(max_acc_len)]) + "\t" + \
                     "\t".join(["neutral" + str(_ + 1) + "_share" for _ in range(max_neutral_len)]) + "\n"
        results_file = self.build_name(prefix="runs_")
        results = open(results_file, 'w')
        results.write(results_first_line)
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_runs_object = file_result[1]['runs']  # this is a dictionary - I select key 'runs'
            print(temp_runs_object.neutral_runs)
            res_line = file_name + "\t"
            res_line += "\t".join([str(_) for _ in (temp_runs_object.dec_runs + [0] * (max_dec_len - len(temp_runs_object.dec_runs)))]) + "\t" + \
                       "\t".join([str(_) for _ in (temp_runs_object.acc_runs + [0] * (max_acc_len - len(temp_runs_object.acc_runs)))]) + "\t" + \
                        "\t".join([str(_) for _ in (temp_runs_object.neutral_runs + [0] * (max_neutral_len - len(temp_runs_object.neutral_runs)))])
            res_line += "\n" if not self.runs_shares else "\t" + "\t".join([str(_) for _ in (temp_runs_object.dec_runs_share + [0] * (max_dec_len - len(temp_runs_object.dec_runs_share)))]) + "\t" + \
                       "\t".join([str(_) for _ in (temp_runs_object.acc_runs_share + [0] * (max_acc_len - len(temp_runs_object.acc_runs_share)))]) + "\t" + \
                        "\t".join([str(_) for _ in (temp_runs_object.neutral_runs_share + [0] * (max_neutral_len - len(temp_runs_object.neutral_runs)))]) + "\n"
            print(res_line)
            results.write(res_line)
        results.close()

    def dump_spectrum(self, bands=[0, 0.003, 0.04, 0.15, 0.4], ulf = True, dump = True):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the LS_spectrum for each
        file in the project
        :return:
        """
        results_first_line = 'file_name\t'
        if not ulf:
            bands = [0, 0.04, 0.15, 0.4]
            results_first_line += "ULF\tLF\tHF\tTP\tLF/HF\n"
        else: 
            results_first_line += "VLF\tULF\tLF\tHF\tTP\tLF/HF\n"
        results_file = self.build_name(prefix=self.spectrum_type + "_spectrum_")
        if dump : results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_spectral_results_object = file_result[1]['Spectrum']
            temp_spectral_results_for_file = list(temp_spectral_results_object.spectrum.get_bands(ulf = ulf).values())
            results_line = file_name + '\t' + "\t".join(map(str, temp_spectral_results_for_file))+ "\t" + str(temp_spectral_results_object.spectrum.LF_HF_ratio) + "\n"
            if dump: results.write(results_line)
            all_results.append(results_line)
        if dump: results.close()
        #return temp_spectral_results_for_file
        return(results_first_line, all_results)

    def dump_quality(self):
        results_first_line = 'file_name\tn_total\tn_sinus\tn_ventricular\tn_supraventricular\tn_artifact\tn_unknown\n'
        results_file = self.build_name(prefix="Quality_")
        results = open(results_file, 'w')
        results.write(results_first_line)
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_quality_object = file_result[1]['Quality']
            res_line = file_name + '\t' + '\t'.join([str(_) for _ in temp_quality_object]) + '\n'
            results.write(res_line)
        results.close()

    def build_name(self, prefix=""):
        import datetime
        import os
        """
        this function builds the name of the results file - the aim is to leave the existing results files_list
        """
        current_name = self.path + "/" + prefix + "results_"+str(datetime.date.today())+".csv"
        i = 1
        while (True):
            if os.path.exists(current_name):
                current_name = self.path + "/" + prefix + "results_" + str(datetime.date.today()) + "_" + str(i) + ".csv"
            else:
                break
            i += 1
        return current_name

    def find_longest_runs(self):
        """
        this function looks for the longest run of a type WITHIN a PROJECT
        """
        longest_dec_run = max([len(_[1]["runs"].dec_runs) for _ in self.project_results]) # _ is obviously dummy
        longest_acc_run = max([len(_[1]["runs"].acc_runs) for _ in self.project_results])
        longest_neutral_run = max([len(_[1]["runs"].neutral_runs) for _ in self.project_results])
        return longest_dec_run, longest_acc_run, longest_neutral_run


