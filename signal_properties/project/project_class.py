

class Project:
    def __init__(self):
        self.path = None
        self.file_extension = None
        self.column_signal = None
        self.column_annot = None
        self.column_sample_to_sample = None
        self.quotient_filter = -1
        self.square_filter=(-8000, 8000)
        self.annotation_filter=()
        self.file_list = []
        