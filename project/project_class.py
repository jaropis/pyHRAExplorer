from glob import glob

class Project:
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

    def get_files_list(self):
        self.files_list = glob(self.path+'/*'+self.file_extension)