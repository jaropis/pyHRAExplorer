from re import findall
from scipy import array, where, cumsum
from signal_properties.Poincare import Poincare
from signal_properties.runs import Runs
from signal_properties.spectral import LombScargleSpectrum



class Signal: ### uwaga! timetrack! dodac, przetestowac, zdefiniowac wyjatek, podniesc wyjatek w spectrum gdy nie ma timetracka!
    def __init__(self, path_to_file, column_signal=0, column_annot=0, column_sample_to_sample=0, quotient_filter=-1, square_filter=(-8000, 8000), annotation_filter=()):
        # 0 are there to facilitate the construction of signals from console
        self.quotient_filter = quotient_filter
        self.square_filter = square_filter
        self.annotation_filter = annotation_filter
        self.signal, self.annotation, self.timetrack = self.read_data(path_to_file, column_signal, column_annot,
                                                                             column_sample_to_sample)
        # here the data is filtered - this filtration will apply throughout the whole application
        self.filter_data()

        # now the HRV and HRA methods are being applied

        self.poincare = None
        self.runs = None
        self.LS_spectrum = None

    def read_data(self, path_to_file, column_signal, column_annot, column_sample_to_sample):
        if type(path_to_file) == list:
            if len(path_to_file) == 2:
                # this is the possibility to pass a list with signal and annotation vector as its elements
                return array(path_to_file[0]), array(path_to_file[1]), cumsum(array(path_to_file[0]))
            else:
                return array(path_to_file[0]), array(path_to_file[1]), array(path_to_file[2])
        reafile_current = open(path_to_file, 'r')
        reafile_current.readline()
        signal = []  # this variable contains the signal for spectral analysis
        annotation = []
        sample_to_sample = [] # this variable holds the sample-to-sample values (like the beat-to-beat interval,
        # RR interval) - this will be used in the Lomb-Scargle periodogram, which requires the time-track column
        # here the reading of the file starts

        for line in reafile_current:
            line_content = findall(r'\b[0-9\.]+', line)
            signal.append(float(line_content[column_signal]))
            if column_signal != column_annot:  # see below - similar condition
                annotation.append(int(float(line_content[column_annot])))
            if column_sample_to_sample !=0 and column_sample_to_sample != column_signal:
                sample_to_sample.append(float(line_content[column_sample_to_sample]))
        signal = array(signal)
        if column_sample_to_sample == column_signal:
            sample_to_sample = signal
 
        timetrack = cumsum(sample_to_sample)

        if column_signal == column_annot:
            annotation = 0*signal
        annotation = array(annotation)
        reafile_current.close()
        return signal, annotation, timetrack

    def filter_data(self):
        """
        this function defines the filter method. It uses the following parameters accepted by the constructor:
        quotient - parameters of the quotient filter - the rejectance ratio - the initial value of -1 means "do not filter"
        square - parameters of the square filter
        annotation - parameters of the annotation filter - 1 means "remove from analysis" and refers to
        (sinus, ventricular, supraventricular, artifact) respectively
        """

        # now, let the filtering begin
        # beginning with the annotation filter
        # 16 henceforth means "bad"
        if len(self.annotation_filter)>0:
            for beat_type in self.annotation_filter:
                self.annotation[where(self.annotation == beat_type)] = 16

        # now the square filter
        self.annotation[where(self.signal < self.square_filter[0])[0]] = 16
        self.annotation[where(self.signal > self.square_filter[1])[0]] = 16

        # now removing bad beats from the beginning and the end of the recording
        try:
            while self.annotation[0] != 0:
                self.signal = self.signal[1:]
                self.annotation = self.annotation[1:]
                self.timetrack = self.timetrack[1:]

            # removing nonsinus beats from the end
            while self.annotation[-1]!=0:
                self.signal=self.signal[0:-1]
                self.annotation=self.annotation[0:-1]
                self.timetrack=self.timetrack[0:-1]
        except IndexError:
            print("no good beats")

        return None

    def set_poincare(self):
        self.poincare = Poincare(self)

    def set_runs(self):
        self.runs = Runs(self)

    def set_LS_spectrum(self):
        self.LS_spectrum = LombScargleSpectrum(self)
