from scipy import array, where
from re import findall
from numpy import concatenate, delete

class Signal:
    def __init__(self, path_to_file, column_signal=0, column_annot=0, quotient_filter=-1, square_filter=(0, 8000), annotation_filter=()):
        # 0 are there to facilitate the construction of signals from console
        self.signal, self.annotation = self.read_data(path_to_file, column_signal, column_annot)
        self.quotient_filter = quotient_filter
        self.square_filter = square_filter
        self.annotation_filter = annotation_filter
        self.annotation_filter = annotation_filter
        self.poincare = Poincare(self)
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

class Poincare:
    def __init__(self, signal):
        ### signal is object of Signal class
        self.xi, self.xii = self.filter_and_prepare(signal)

    def filter_and_prepare(self, signal):
        """
        this function defines the filter method. It accepts the following parameters:
        quotient - parameters of the quotient filter - the rejectance ratio - the initial value of -1 means "do not filter"
        square - parameters of the square filter
        annotation - parameters of the annotation filter - 1 means "remove from analysis" and refers to
        (sinus, ventricular, supraventricular, artifact) respectively
        a filtered Poincare plot is returned
        the method follows "Filtering Poincare plots", Piskorski, Guzik, Computational methods in science and technology 11 (1), 39-48
        """
        # beginning with the annotation filter
        # 16 henceforth means "bad"
        if len(signal.annotation_filter)>0:
            for beat_type in signal.annotation_filter:
                signal.annotation[where(signal.annotation == beat_type)] = 16

        # now the square filter
        signal.annotation[where(signal.signal < signal.square_filter[0])[0]] = 16
        signal.annotation[where(signal.signal > signal.square_filter[1])[0]] = 16

        # now removing bad beats from the beginning and the end of the recording
        try:
            while signal.annotation[0]!=0:
                signal.signal=signal.signal[1:]
                signal.annotation=signal.annotation[1:]

            # removing nonsinus beats from the end
            while signal.annotation[-1]!=0:
                signal.signal=signal.signal[0:-1]
                signal.annotation=signal.annotation[0:-1]
        except IndexError:
            print("no good beats")

        # preparing the Poincare plot auxiliary vectors (see Filtering Poincare Plots)
        xi = signal.signal[0:(len(signal.signal)-1)]
        xii = signal.signal[1:len(signal.signal)]

        bad_beats = where(signal.annotation == 16)[0]
        bad_beats_minus_one = bad_beats - 1
        all_bad_beats = concatenate((bad_beats, bad_beats_minus_one))

        # now removing all bad beats from xi and xii, according to the above paper
        xi = delete(xi, all_bad_beats)
        xii = delete(xii, all_bad_beats)

        return xi, xii