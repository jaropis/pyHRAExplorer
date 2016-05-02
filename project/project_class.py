from glob import glob

class Project:
    """
    This class separates the data from the GUI and from the mathematics. It operates on the mathematics and communicates
    with the GUI.
    """
    def __init__(self, path, file_extension):
        self.path = path
        self.file_extension = file_extension
        self.column_signal = None
        self.column_annot = None
        self.column_sample_to_sample = None
        self.quotient_filter = -1
        self.square_filter=(-8000, 8000)
        self.annotation_filter=()
        self.files_list = []

        self.Poincare_state = 0
        self.runs_state = 0
        self.LS_spectrum_state = 0

        self.results = {Poincare: [], runs: [], LS_spectrum: []}
        
    def get_files_list(self):
        """
        build a list of the files associated with the project, i.e. in the correct directory, with the correct
        extension
        """
        self.files_list = glob(self.path+'/*'+self.file_extension)

    def set_Poincare(self):
        """
        this means: calculate the Poincare descriptors
        """
        self.Poincare_state = 1

    def set_runs(self):
        """
        this means: calculate runs
        """
        self.runs_state = 1

    def set_LS_spectrum(self):
        """
        this means: calculate Lomb-Scargle spectrum
        """
        self.LS_spectrum_state = 1

    def set_columns(self, column_signal=None, column_annotation=None, column_sample_to_sample=None):
        """
        sets the columns in the files
        :param column_signal: the number of the column holding the signal
        :param column_annotation: the number of the column holdng the annotations
        :param column_sample_to_sample: the number of the column holding the sample-to-sample values
        :return:
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
        pass
