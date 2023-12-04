from glob import glob
from signal_properties.RRclasses import Signal

class Project:
    """
    This class separates the data from the GUI and from the mathematics. It operates on the mathematics and communicates
    with the GUI.
    The main method of the Class is the step_thorugh_project class which goes over all the files in a project (folder
    with files), and calculates the HRV/HRA properties of the files

    Attributes:
        project_name (str): Name of the project
        path (str): Path to the files for the analysis
        file_extension (str): Extension of the files for analysis
        column_signal (int): the number of the column holding the signal
        column_annotation (int): the number of the column holdng the annotations
        column_sample_to_sample (int): the number of the column holding the sample-to-sample values
        annotation_filter (tuple): sets the tuple holding annotations to remove
        square_filter (tuple): sets the upper and lower values to cut
        quotient_filter (int): sets the quotient under/over which to remove a beat (sample)
        files_list (list): List of files for the analysis
        Poincare_state (bool): Caluclates Poincare results when True
        pnn_state (bool): Caluclates pNN and pNN% results when True
        runs_state (bool): Caluclates Runs results when True
        spectrum_state (bool): Caluclates Spectrum results when True
        quality_state (bool): Caluclates Qulity results when True
        project_results (dict): A dictionary with results, results = {Poincare: [], runs: [], LS_spectrum: []} - a list may be empty if the user
        does not want a specific type of result

    """
    def __init__(self, path, file_extension, column_signal, column_annot, column_sample_to_sample):
        self.project_name = None
        self.path = path
        self.file_extension = file_extension
        self.column_signal = column_signal
        self.column_annot = column_annot
        self.column_sample_to_sample = column_sample_to_sample
        self.quotient_filter = -1
        self.square_filter = (-8000, 8000)
        self.annotation_filter = ()
        self.files_list = self.get_files_list()

        # these three flags say whether or not the specific method should be used
        self.Poincare_state = False
        self.pnn_state = False
        self.pnn_range_state = False
        self.runs_state = False
        self.spectrum_state = False
        self.spectrum_type = 'None'
        self.quality_state = False

        self.project_results = [] # this list of lists will hold the name of the file and the self.file_results for
        # each file eg. [[filename1, {Poincare: , runs: , LS_spectrum}], [filename2, {Poincare: , runs: , LS_spectrum}}

    def get_files_list(self):
        """
        build a list of the files associated with the project, i.e. in the correct directory, with the correct
        extension

        Returns:
            files_list (list): List of files for the analysis
        """
        #return [item.split("/")[-1] for item in glob(self.path+'/*'+self.file_extension)]
        files_list = [item.split("\\")[-1] for item in glob(self.path+'/*'+self.file_extension)]
        return files_list

    def set_Poincare(self):
        """
        When called this method sets the Poincare state to True, This means: calculate the Poincare descriptors
        """
        self.Poincare_state = True

    def set_pnn(self):
        """
        When called this method sets the pNN state to True, This means: calculate the pNN and pNN percent descriptors
        """
        self.pnn_state = True

    def set_pnn_range(self):
        """
        When called this method sets the pNN state to True, This means: calculate the pNN ranges descriptors
        """
        self.pnn_range_state = True


    def set_runs(self):
        """
        When called this method sets the Runs state to True, This means: calculate runs
        """
        self.runs_state = True
    
    def set_spectrum(self, spectrum_type = 'LS'):
        """
        When called this method sets the Spectrum state to True, This means: calculate spectrum, can be either Lombscargel (LS) or Welch type

        Arguments:
            spectrum_type (str): A string describing the type of spectrum, either 'LS' for Lomb-Scargle or 'Welch' for Welch are recognised.
        """
        self.spectrum_state = True
        self.spectrum_type = spectrum_type

    def set_quality(self):
        """
        When called this method sets the Quality state to True, This means: calculate quality parameters (number of beats if each type)
        """
        self.quality_state = True

    def set_columns(self, column_signal=None, column_annotation=None, column_sample_to_sample=None):
        """
        This method sets the columns in the files
        
        Arguments:
            column_signal (int): the number of the column holding the signal
            column_annotation (int): the number of the column holdng the annotations
            column_sample_to_sample (int): the number of the column holding the sample-to-sample values
        
        Returns:
            does not return anything - just modifies the arguments
        """
        self.column_signal = column_signal
        self.column_annot = column_annotation
        self.column_sample_to_sample = column_sample_to_sample

    def set_filters(self, annotation_filter=(), square_filter=(-8000, 8000), quotient_filter=-1):
        """
        This method sets the filters
        
        Arguments:
            annotation_filter (tuple): sets the tuple holding annotations to remove
            square_filter (tuple): sets the upper and lower values to cut
            quotient_filter (int): sets the quotient under/over which to remove a beat (sample)
        
        Returns:
            does not return anything
        """
        self.annotation_filter = annotation_filter
        self.square_filter = square_filter
        self.quotient_filter = quotient_filter

    def step_through_project_files(self):
        """
        This is the main method of this class - it visits every file and, if the _state variable is 1 calculates
        the respective HRV/HRA method
        
        Returns:
            project_results (dict): A dictionary with results, results = {Poincare: [], runs: [], LS_spectrum: []} - a list may be empty if the user
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
            if self.Poincare_state or self.pnn_state or self.pnn_range_state:
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

            if self.quality_state:
                temp_quality = temp_signal.quality_counts
            temp_file_results = {"Poincare": temp_poincare, "runs": temp_runs, "Spectrum": temp_spectrum, 'Quality': temp_quality}
            self.project_results.append([file, temp_file_results])

    # methods to finish
    def read_state(self):
        """
        This method checks if the project already exists, reads from the .project files the state of the project, and,
        if some of the calculations have already been performed, it prevents the Project from re-doing them
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
            self.spectrum_state = bool(input_file.readline().split(':')[1].rstrip())
            self.quality_state = bool(input_file.readline().split(':')[1].rstrip())
            self.pnn_state = bool(input_file.readline().split(':')[1].rstrip())
            self.pnn_range_state = bool(input_file.readline().split(':')[1].rstrip())
            input_file.close()
            return(True)
        except Exception:
            return(False)

    def write_state(self):
        """
        This method writes the state of the project to the drive
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
            output_line += "Spectrum state:" + str(int(self.spectrum_state)) + "\n"
            output_line += "Spectrum type:" + self.spectrum_type + "\n"
            output_line += "Quality state:" + str(int(self.quality_state)) + "\n"
            output_line += "pNN state:" + str(int(self.pnn_state)) + "\n"
            output_line += "pNN range state:" + str(int(self.pnn_range_state)) + "\n"
            output_file.write(output_line)
            output_file.close()
            return True
        except Exception:
            return False

    def dump_Poincare(self, dump = True):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the Poincare plot descriptors for each
        file in the project

        Arguments:
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file
        """
        #results_first_line = "filename\tSDNN\tSD1\tSD2\tSD1d\tSD1a\tC1d\tC1a\tSD2d\tSD2a\tC2d\tC2a\tSDNNd\tSDNNa\tCd\tCa\n"
        results_first_line = "filename\tSDNN\tSD1\tSD2\tSD2/SD1\tmeanRR\tpNN50\tSD1d\tC1d\tSD1a\tC1a\tSD1I\tND\tSD2d\tC2d\tSD2a\tC2a\tSD2I\tSDNNd\tCd\tSDNNa\tCa\tHRA1\tHRA2\tHRAT\tHRAN\tHRAcomp\tCS\tCSa\tCSd\tCLa\tCLd\n"
        results_file = self.build_name(prefix="Poincare_")
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_poincare_object = file_result[1]['Poincare'] # this is a dictionary - I select key Poincare
            res_line = file_name + "\t"
            res_line += str(temp_poincare_object.SDNN) + "\t" + str(temp_poincare_object.SD1) + "\t" + str(temp_poincare_object.SD2) + "\t" + \
                str(temp_poincare_object.SD2_SD1) + "\t" + str(temp_poincare_object.meanRR) + "\t" + str(temp_poincare_object.pNN50) + "\t"+ \
                    "\t".join([str(_) for _ in temp_poincare_object.short_term_asymmetry()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.long_term_asymmetry()]) + \
                    "\t" + "\t".join([str(_) for _ in temp_poincare_object.total_asymmetry()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.hra_forms()]) + \
                    "\t" + "\t".join([str(_) for _ in temp_poincare_object.short_term_variability()]) + "\t" + "\t".join([str(_) for _ in temp_poincare_object.long_term_variability()]) + "\n"
            if dump: results.write(res_line)
            all_results.append(res_line)
        if dump: results.close()
        return(results_first_line, all_results)
        
    def dump_pnn(self, max_pnn = 100, pnn_step = 10, max_pnn_pro = 10, pnn_pro_step = 0.5, add_dec_acc = False, dump = True):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the pNN series (from 0 ms to specified (100 by default)ms, every 10 ms) and 
        pNN_procent series (from 0.5 % to specified (10 by default)%, every 0.5%) for for each file in the project
        
        Arguments:
            max_pnn (int): Maximum pNN, 100 ms by default
            pnn_step (int): Step for each consequtive pNN, 10 by default
            max_pnn_pro (int): Maximum pNN procent, 10% by deaulft
            pnn_pro_step (float): Step for each consequtive pNN%, 0.5 by default
            add_dec_acc (bool): Determines if pNN and pNN% should also be calculated for decelerating and accelerating beats separately
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file        
        """
        max_pnn = max_pnn
        results_file = self.build_name(prefix="PNN_" if not add_dec_acc else "PNN_DEC_ACC_")
        results_first_line = 'filename\t' + "PNN_neutral" + "\t" + "\t".join("pNN_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step))
        # Adding optional PNNs for dec and acc 
        results_first_line += "\t" if not add_dec_acc else "\t" + "\t".join("pNN_dec_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step)) + \
        "\t" + "\t".join("pNN_acc_" + str(_) for _ in range(0, max_pnn + pnn_step, pnn_step))
        # Adding pNN%
        results_first_line += "\t" + "\t".join("pNN_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step)))
        # Adding optional pNN% for dec and acc
        results_first_line += "\n" if not add_dec_acc else "\t" + "\t".join("pNN_dec_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + \
            "\t" + "\t".join("pNN_acc_" + str(_/10) + "%" for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + "\n"
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            res_line = file_name
            temp_poincare_object = file_result[1]['Poincare']
            res_line += "\t" + str(temp_poincare_object.pNN_neutral) + "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[0]) for _ in range(0, max_pnn + pnn_step, pnn_step))
            # Optional results for dec and acc
            res_line += "\t" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[1]) for _ in range(0, max_pnn + pnn_step, pnn_step)) + \
             "\t" + "\t".join(str(temp_poincare_object.pnnx(_)[2]) for _ in range(0, max_pnn + pnn_step, pnn_step)) + "\t"
            res_line += "\t".join(str(temp_poincare_object.pnn_pro(_/10)[0]) for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step)))
            # Optional results for dec and acc
            res_line += "\n" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnn_pro(_/10)[1]) for _ in range(5, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + \
            "\t" + "\t".join(str(temp_poincare_object.pnn_pro(_/10)[2]) for _ in range(10*pnn_pro_step, int(10*(max_pnn_pro + pnn_pro_step)), int(10*pnn_pro_step))) + "\n"
            if dump: results.write(res_line)
            all_results.append(res_line)
            #temp_poincare_object.pnnx()[0]
            #temp_poincare_object.pnn_pro()[0]
        if dump: results.close()
        return [results_first_line, all_results]
    
    def dump_pNN_range(self, start = 0, end = 100, step = 10, add_dec_acc = False, dump = False):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the pNN within a specified range (atart <= pNN < end) 
        for for each file in the project
        
        Arguments:
            start (int): Start of pNN range
            end (int): End of pNN range (end itself is not part of range)
            final (int): Returns all >= x when specified (range x to inf)
            add_dec_acc (bool): Determines if pNN in ranges also be calculated for decelerating and accelerating beats separately
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file        
        """
        results_file = self.build_name(prefix="PNN_range_" if not add_dec_acc else "PNN_range_DEC_ACC_")
        results_first_line = 'filename\t' + "\t".join("pNN_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + \
        "\tpNN" + str(end) + "+"
        # Adding optional PNNs for dec and acc 
        results_first_line += "\n" if not add_dec_acc else "\t" + "\t".join("pNN_dec_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + \
         "\tpNN_dec_" + str(end) + "+\t" + "\t".join("pNN_acc_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + "\tpNN_acc_" + str(end) + "+\n"
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        test = []
        for file_result in self.project_results:
            file_name = file_result[0]
            res_line = file_name
            temp_poincare_object = file_result[1]['Poincare']
            res_line += "\t" + "\t".join(str(temp_poincare_object.pnn_range(x1 = _, x2 = _+step, final = end)[0]) for _ in range(start,end+step,step))
            # Optional results for dec and acc
            res_line += "\n" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnn_range(x1 = _, x2 = _+step, final = end)[1]) for _ in range(start,end+step,step)) + \
             "\t" + "\t".join(str(temp_poincare_object.pnn_range(x1 = _, x2 = _+step, final = end)[2]) for _ in range(start,end+step,step)) + "\n"
            if dump: results.write(res_line)
            all_results.append(res_line)
        if dump: results.close()
        return [results_first_line, all_results]
    
    def dump_pNN_range_pro(self, start = 0, end = 10, step = 1, add_dec_acc = False, dump = False):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the pNN within a specified % range (atart <= pNN < end) 
        for for each file in the project
        
        Arguments:
            start (int): Start of pNN % range
            end (int): End of pNN % range (end itself is not part of range)
            final (int): Returns all >= x when specified (range x to inf)
            add_dec_acc (bool): Determines if pNN % in ranges also be calculated for decelerating and accelerating beats separately
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file        
        """
        results_file = self.build_name(prefix="PNN_range_pro" if not add_dec_acc else "PNN_range_pro_DEC_ACC_")
        results_first_line = 'filename\t' + "\t".join("pNN%_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + \
        "\tpNN" + str(end) + "+"
        # Adding optional PNNs for dec and acc 
        results_first_line += "\n" if not add_dec_acc else "\t" + "\t".join("pNN%_dec_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + \
         "\tpNN_dec_" + str(end) + "+\t" + "\t".join("pNN%_acc_" + str(_) + "_" + str(_+step) for _ in range(start, end, step)) + "\tpNN_acc_" + str(end) + "+\n"
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        test = []
        for file_result in self.project_results:
            file_name = file_result[0]
            res_line = file_name
            temp_poincare_object = file_result[1]['Poincare']
            res_line += "\t" + "\t".join(str(temp_poincare_object.pnn_range_pro(x1 = _, x2 = _+step, final = end)[0]) for _ in range(start,end+step,step))
            # Optional results for dec and acc
            res_line += "\n" if not add_dec_acc else "\t" + "\t".join(str(temp_poincare_object.pnn_range_pro(x1 = _, x2 = _+step, final = end)[1]) for _ in range(start,end+step,step)) + \
             "\t" + "\t".join(str(temp_poincare_object.pnn_range_pro(x1 = _, x2 = _+step, final = end)[2]) for _ in range(start,end+step,step)) + "\n"
            if dump: results.write(res_line)
            all_results.append(res_line)
        if dump: results.close()
        return [results_first_line, all_results]
        
    def dump_runs(self, runs_shares = False, dump = True):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the monotonic runs for each
        file in the project
        
        Arguments:
            runs_shares (bool): Returns the shares of each run type against all the runs, False by default
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file        
        """
        max_dec_len, max_acc_len, max_neutral_len = self.find_longest_runs()
        print(max_dec_len, max_acc_len, max_neutral_len)
        results_first_line = "file_name" + "\t" + "\t".join(["dec"+str(_+1) for _ in range(max_dec_len)]) + "\t"+ \
                     "\t".join(["acc" + str(_ + 1) for _ in range(max_acc_len)]) + "\t" + \
                     "\t".join(["neutral" + str(_ + 1) for _ in range(max_neutral_len)])
        results_first_line += "\n" if not runs_shares else "\t" + "\t".join(["dec"+str(_+1)+"_share" for _ in range(max_dec_len)]) + "\t"+ \
                     "\t".join(["acc" + str(_ + 1) + "_share" for _ in range(max_acc_len)]) + "\t" + \
                     "\t".join(["neutral" + str(_ + 1) + "_share" for _ in range(max_neutral_len)]) + "\n"
        results_file = self.build_name(prefix="runs_")
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_runs_object = file_result[1]['runs']  # this is a dictionary - I select key 'runs'
            res_line = file_name + "\t"
            res_line += "\t".join([str(_) for _ in (temp_runs_object.dec_runs + [0] * (max_dec_len - len(temp_runs_object.dec_runs)))]) + "\t" + \
                       "\t".join([str(_) for _ in (temp_runs_object.acc_runs + [0] * (max_acc_len - len(temp_runs_object.acc_runs)))]) + "\t" + \
                        "\t".join([str(_) for _ in (temp_runs_object.neutral_runs + [0] * (max_neutral_len - len(temp_runs_object.neutral_runs)))])
            res_line += "\n" if not runs_shares else "\t" + "\t".join([str(_) for _ in (temp_runs_object.dec_runs_share + [0] * (max_dec_len - len(temp_runs_object.dec_runs_share)))]) + "\t" + \
                       "\t".join([str(_) for _ in (temp_runs_object.acc_runs_share + [0] * (max_acc_len - len(temp_runs_object.acc_runs_share)))]) + "\t" + \
                        "\t".join([str(_) for _ in (temp_runs_object.neutral_runs_share + [0] * (max_neutral_len - len(temp_runs_object.neutral_runs)))]) + "\n"
            all_results.append(res_line)
            if dump: results.write(res_line)
        if dump: results.close()
        return(results_first_line, all_results)

    def dump_spectrum(self, bands=[0, 0.003, 0.04, 0.15, 0.4], ulf = True, dump = True):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the Spectrum for each
        file in the project

        Arguments:
            bands (list): List of values of bands for spectral analysis
            ulf (bool): Dtermines if bands are calculated with or without ulf, True by default
            dump (bool): Determines if the file is written (used when all the results are combined together), True by default
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file   
        """
        results_first_line = 'file_name\t'
        if not ulf:
            bands = [0, 0.04, 0.15, 0.4]
            results_first_line += "VLF\tLF\tHF\tTP\tLF/HF\n"
        else: 
            results_first_line += "ULF\tVLF\tLF\tHF\tTP\tLF/HF\n"
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

    def dump_quality(self, dump = True):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains the Quality results for each
        file in the project (Number of all, sinus, ventricular, supraventricular, artifact and unknown beats)

        Arguments:
            dump (bool): Determines if the file is written (used when all the results are combined together)
        
        Returns:
            results_first_line (str): A string with the header for the results
            all_results (list): A list of all the strings with results for each file        
        """
        results_first_line = 'file_name\tn_total\tn_sinus\tn_ventricular\tn_supraventricular\tn_artifact\tn_unknown\n'
        results_file = self.build_name(prefix="Quality_")
        if dump: results = open(results_file, 'w'); results.write(results_first_line)
        all_results = []
        for file_result in self.project_results:
            file_name = file_result[0]
            temp_quality_object = file_result[1]['Quality']
            res_line = file_name + '\t' + '\t'.join([str(_) for _ in temp_quality_object]) + '\n'
            if dump: results.write(res_line)
            all_results.append(res_line)
        if dump: results.close()
        return(results_first_line, all_results)

    def build_name(self, prefix=""):
        import datetime
        import os
        """
        This method builds the name of the results file - the aim is to leave the existing results files_list

        Returns:
            current_name (str): String containg the Name of the results file.
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
        This method looks for the longest run of a type within a project

        Returns:
            longest_dec_run (int): An integer storing the length of the longest dec run in the project (max number of consequtive beats of the dec type)
            longest_acc_run (int): An integer storing the length of the longest acc run in the project (max number of consequtive beats of the acc type)
            longest_neutral_run (int): An integer storing the length of the longest neutral run in the project (max number of consequtive beats of the neutral type)
        """
        longest_dec_run = max([len(_[1]["runs"].dec_runs) for _ in self.project_results]) # _ is obviously dummy
        longest_acc_run = max([len(_[1]["runs"].acc_runs) for _ in self.project_results])
        longest_neutral_run = max([len(_[1]["runs"].neutral_runs) for _ in self.project_results])
        return longest_dec_run, longest_acc_run, longest_neutral_run

    def dump_all(self, bands=[0, 0.003, 0.04, 0.15, 0.4], ulf = True, runs_shares = False, max_pnn = 100, pnn_step = 10, max_pnn_pro = 10, pnn_pro_step = 0.5, add_dec_acc = False, start = 0, end = 100, step = 10, pnn_range_type = 'number'):
        """
        This method writes a csv/xlsx/ods file to the disk - this file contains all the results from analyses with active states

        Arguments:
            
            bands (list): List of values of bands for spectral analysis
            ulf (bool): Dtermines if bands are calculated with or without ulf, True by defaultmax_pnn (int): Maximum pNN, 100 ms by default
            runs_shares (bool): Returns the shares of each run type against all the runs, False by default
            pnn_step (int): Step for each consequtive pNN, 10 by default
            max_pnn_pro (int): Maximum pNN procent, 10% by deaulft
            pnn_pro_step (float): Step for each consequtive pNN%, 0.5 by default
            add_dec_acc (bool): Determines if pNN and pNN% should also be calculated for decelerating and accelerating beats separately
            pnn_range_type (str): Determines if the used range is of procent or number type and calls the according method
            
        """
        results_file = self.build_name(prefix="ALL_")
        results = open(results_file, 'w')

        Poincare = self.dump_Poincare(dump = False) if self.Poincare_state else None 
        runs = self.dump_runs(runs_shares = runs_shares, dump = False) if self.runs_state else None 
        spectrum = self.dump_spectrum(bands = bands, ulf = ulf, dump = False) if self.spectrum_state else None 
        pnn = self.dump_pnn(max_pnn = max_pnn, pnn_step = pnn_step, max_pnn_pro = max_pnn_pro, pnn_pro_step = pnn_pro_step, add_dec_acc = add_dec_acc, dump = False) if self.pnn_state else None 
        pnn_range = self.dump_pNN_range(start = start, end = end, step = step, add_dec_acc = add_dec_acc, dump = False) if self.pnn_range_state and pnn_range_type == 'number' else self.dump_pNN_range_pro(start = start, end = end, step = step, add_dec_acc = add_dec_acc, dump = False) if self.pnn_range_state and self.pnn_range_type == 'procent' else None
        quality = self.dump_quality(dump = False) if self.quality_state else None

        all_filenames = []
        all_results = []
        for result in [Poincare, runs, spectrum, pnn, pnn_range, quality]:
            if result is not None:
                all_filenames.append(result[0])
                all_results.append(result[1])

        first_line = "file_name" + "\t" + "\t".join((_[_.find('\t')+1:_.find('\n')]) for _ in all_filenames) + "\n"
        results.write(first_line)
        for n in range(0, len(self.files_list)):
            result = self.files_list[n] + "\t" + "\t".join((_[_.find('\t')+1:_.find('\n')]) for _ in [res[n] for res in all_results]) + "\n"
            results.write(result)
        results.close()
