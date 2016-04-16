from re import findall
from Poincare import Poincare
from scipy import array


class Signal:
    def __init__(self, path_to_file, column_signal=0, column_annot=0, quotient_filter=-1, square_filter=(0, 8000), annotation_filter=()):
        # 0 are there to facilitate the construction of signals from console
        self.signal, self.annotation = self.read_data(path_to_file, column_signal, column_annot)
        self.quotient_filter = quotient_filter
        self.square_filter = square_filter
        self.annotation_filter = annotation_filter
        self.annotation_filter = annotation_filter
        self.poincare = Poincare(self)
        self.runs = Runs(self)
        # runs = Runs(self)
        # spectrum = Spectrum(self)

    def read_data(self, path_to_file, column_signal, column_annot):
        if type(path_to_file) == list:
            # this is the possibility to pass a list with signal and annotation vector as its elements
            return array(path_to_file[0]), array(path_to_file[1])
        reafile_current = open(path_to_file, 'r')
        reafile_current.readline()
        signal = []  # this variable contains the signal for spectral analysis
        annotation = []
        # here the reading of the file starts
        for line in reafile_current:
            line_content = findall(r'\b[0-9\.]+', line)
            signal.append(float(line_content[column_signal-1]))
            if column_signal != column_annot:  # see below - similar condition
                annotation.append(int(float(line_content[column_annot-1])))
        signal = array(signal)
        if column_signal == column_annot:
            annotation = 0*signal
        annotation = array(annotation)
        return signal, annotation