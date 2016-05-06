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
        self.runs_state = False
        self.LS_spectrum_state = False

        self.project_results = [] # this list of lists will hold the name of the file and the self.file_results for
        # each file eg. [[filename1, {Poincare: , runs: , LS_spectrum}], [filename2, {Poincare: , runs: , LS_spectrum}}

    def get_files_list(self):
        """
        build a list of the files associated with the project, i.e. in the correct directory, with the correct
        extension
        """
        return [item.split("/")[-1] for item in glob(self.path+'/*'+self.file_extension)]

    def set_Poincare(self):
        """
        this means: calculate the Poincare descriptors
        """
        self.Poincare_state = True

    def set_runs(self):
        """
        this means: calculate runs
        """
        self.runs_state = True

    def set_LS_spectrum(self):
        """
        this means: calculate Lomb-Scargle spectrum
        """
        self.LS_spectrum_state = True

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
        for file in self.files_list:
            temp_path = self.path + "/" + file
            temp_signal = Signal(path_to_file=temp_path, column_annot=self.column_annot, column_signal=self.column_signal,
                                 column_sample_to_sample=self.column_sample_to_sample, annotation_filter=self.annotation_filter,
                                 square_filter=self.square_filter, quotient_filter=self.quotient_filter)
            if self.Poincare_state:
                temp_signal.set_poincare()
                temp_poincare = temp_signal.poincare
            else:
                temp_poincare = None

            if self.runs_state:
                temp_signal.set_runs()
                temp_runs = temp_signal.runs
            else:
                temp_runs = None

            if self.LS_spectrum_state:
                temp_signal.set_LS_spectrum()
                temp_LS_spectrum = None
            temp_file_results = {"Poincare": temp_poincare, "runs": temp_runs, "LS_spectrum": temp_LS_spectrum}
            self.project_results.append[file, temp_file_results] ## question to self - do I need to keep the whole objects
            # in the resulting list??? - correct


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
            print(self.project_name)
            self.files_no = int(input_file.readline().split(':')[1].rstrip())
            print(self.files_no)
            self.column_signal = int(input_file.readline().split(':')[1].rstrip())
            self.column_annot = int(input_file.readline().split(':')[1].rstrip())
            self.column_sample_to_sample = int(input_file.readline().split(':')[1].rstrip())
            self.annotation_filter = eval(input_file.readline().split(':')[1].rstrip())
            self.square_filter = eval(input_file.readline().split(':')[1].rstrip())
            self.quotient_filter = int(input_file.readline().split(':')[1].rstrip())
            self.Poincare_state = bool(input_file.readline().split(':')[1].rstrip())
            self.runs_state = bool(input_file.readline().split(':')[1].rstrip())
            self.LS_spectrum_state = bool(input_file.readline().split(':')[1].rstrip())
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
            output_line += "LS_spectrum state:" + str(int(self.LS_spectrum_state)) + "\n"
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
        pass

    def dump_runs(self):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the monotonic runs for each
        file in the project
        :return:
        """
        pass

    def dump_LS_spectrum(self, bands):
        """
        this method writes a csv/xlsx/ods file to the disk - this file contains the LS_spectrum for each
        file in the project
        :return:
        """
        pass
