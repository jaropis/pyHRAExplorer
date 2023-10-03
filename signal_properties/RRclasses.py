from re import findall
from numpy import array, where, cumsum
from signal_properties.Poincare import Poincare
from signal_properties.runs import Runs
from signal_properties.spectral import LombScargleSpectrum
from signal_properties.plotRR import PlotRR



class Signal: 
    '''
    Signal class used to read, annotate and filter the files contaning the RR signals. Attributes of this class
    are the basis of the HRAExplorer.

    Attributes:
        signal (array): An array containing the values of RR signal
        annotation (array): An array containg the beats flag (0, 1, 2, 3 values corrsponding to sinus, ventricular, supraventricular or artifact beats respecitively)
        that will be used for filtering.
        timetrack (array): An array containing the time track values. Timetrack can be both sample to sample and general, if the first time measurment is equal 0, 
        timetrack is returned without modifications, if given timetrack is sample to sample (amount of time between each sample) cumsum is returned instead.
        quotient_filter (int): the rejectance ratio - the initial value of -1 means "do not filter"
        square_filter (tuple): A tuple containg the values for the square filter, the values indicates 
        the minimal and maximum RR values which are accepted
        annotation_filter (tuple): A tuple containing the flags of bbeats that need to be removed. The 0, 1, 2 and 3 flags refer to 
        sinus, ventricular, supraventricular and artifact respectively
        poincare (None): allows passing the Signal class attributes to the Poincare class methods.
        runs (None): Signal allows passing the class attributes to the Runs class methods.
        LS_spectrum (None): allows passing the Signal class attributes to the LombScargleSpectrum and FFTSpectrum class methods.
        plotRR (None): allows passing the Signal class attributes to the PlotRR class method
    '''
    ### uwaga! timetrack! dodac, przetestowac, zdefiniowac wyjatek, podniesc wyjatek w spectrum gdy nie ma timetracka!
    #changed the defualts to -1 so timetrack can be stored in and called from the first column 
    def __init__(self, path_to_file, column_signal=-1, column_annot=-1, column_sample_to_sample=-1, quotient_filter=-1, square_filter=(-8000, 8000), annotation_filter=()):
        '''
        Initializes the attributes of the Signal class, passing arguments to methods.

        Args:
            path_to_file (str): Path to the file that will be used for the analysis
            column_signal (int): Correstponds to the index (column number - 1) of the column containing the RR 
            the RR signals
            column_annot (int): Corresponds to the index (column number - 1) of the column containg the RR anotations
            that will be used for filtering 
            column_sample_to_sample (int): Corresponds to the index (column number - 1) of the column containing the sample to sample time or time
            quotient_filter (int): the rejectance ratio - the initial value of -1 means "do not filter"
            square_filter (tuple): A tuple containg the values for the square filter, the values indicates 
            the minimal and maximum RR values which are accepted
            annotation_filter (tuple): A tuple containing the flags of bbeats that need to be removed. The 0, 1, 2 and 3 flags refer to 
            sinus, ventricular, supraventricular and artifact respectively

        '''
        # 0 are there to facilitate the construction of signals from console
        self.quotient_filter = quotient_filter
        self.square_filter = square_filter
        self.annotation_filter = annotation_filter
        self.signal, self.annotation, self.timetrack = self.read_data(path_to_file, column_signal, column_annot,
                                                                             column_sample_to_sample)
        # here the data is filtered - this filtration will apply throughout the whole application
        self.filter_data()

        # now the HRV and HRA methods are being applied and plots constructed

        self.poincare = None
        self.runs = None
        self.LS_spectrum = None
        self.plotRR = None

    def read_data(self, path_to_file, column_signal, column_annot, column_sample_to_sample):
        '''
        This method is used to read the file, using the specified column indexes. The default value of the index is -1, so if no value is specified the last column will be used.

        Args:
            path_to_file (str): Path to the file that will be used for the analysis
            column_signal (int): Correstponds to the index (column number - 1) of the column containing the RR 
            the RR signals
            column_annot (int): Corresponds to the index (column number - 1) of the column containg the RR anotations
            that will be used for filtering 
            column_sample_to_sample (int): Corresponds to the index (column number - 1) of the column containing the sample to sample time or time

        Returns:
            signal (array): An array containing the values of RR signal
            annotation (array): An array containg the beats flag (0, 1, 2, 3 values corrsponding to sinus, ventricular, supraventricular or artifact beats respecitively)
            tat will be used for filtering.
            timetrack (array): An array containing the time track values. Timetrack can be both sample to sample and general, if the first time measurment is equal 0, 
            timetrack is returned without modifications, if given timetrack is sample to sample (amount of time between each sample) cumsum is returned instead.
        '''
        if type(path_to_file) == list:
            if len(path_to_file) == 2:
                # this is the possibility to pass a list with signal and annotation vector as its elements
                return array(path_to_file[0]), array(path_to_file[1]), cumsum(array(path_to_file[0]))
            else:
                return array(path_to_file[0]), array(path_to_file[1]), array(path_to_file[2])
        reafile_current = open(path_to_file, 'r')
        reafile_current.readline()
        signal = []  # this variable contains the signal for spectral analysis
        annotation = [] # this variable contains annotations for the signal with 0, 1, 2, 3 values corrsponding 
        # to sinus, ventricular, supraventricular or artifact beats respecitively. Annotations will be used for filtering the beats. 
        sample_to_sample = [] # this variable holds the sample-to-sample values (like the beat-to-beat interval,
        # RR interval) - this will be used in the Lomb-Scargle periodogram, which requires the time-track column
        # here the reading of the file starts

        # Read each line and append each variable with a chosen column
        for line in reafile_current:
            line_content = findall(r'\b[0-9\.]+', line)
            signal.append(float(line_content[column_signal]))
            if column_signal != column_annot:  # see below - similar condition
                # As deafult column index for all is 0, if only one column index or none are specified annotation
                # variable remians empty.
                annotation.append(int(float(line_content[column_annot])))
           
            if column_sample_to_sample !=-1 and column_sample_to_sample != column_signal: # Checks if the column
                # sample to sample has been specified (what is it is in the first column?) maybe change default
                # from 0 to -1?
                sample_to_sample.append(float(line_content[column_sample_to_sample]))
                # added an option for using the sample to sample column with an increasing time (rather than sample to sample time)
                # Changed the way sample to sample/timetrack is assigned
                # If the first row is = 0, the time column shows the progression of time, timetrack can be returned 
                # as is
                if sample_to_sample[0] == 0:
                    timetrack = sample_to_sample
                # If it is not 0, the time column shows sample to sample time, cumsum() of the column should be 
                # returned instead to get the timetrack
                else: 
                    timetrack = cumsum(sample_to_sample)        
            else:
                # To prevent the timetrack not being returned
                timetrack = cumsum(sample_to_sample)
        signal = array(signal)
        if column_sample_to_sample == column_signal:
            sample_to_sample = signal

        #timetrack = cumsum(sample_to_sample)

        if column_signal == column_annot:
            annotation = 0*signal
        annotation = array(annotation)
        reafile_current.close()
        return signal, annotation, timetrack

    def filter_data(self):
        """
        This method filters the signal based on the following filter attributes of the Signal class:
            quotient_filter (int): the rejectance ratio - the initial value of -1 means "do not filter"
            square_filter (tuple): A tuple containg the values for the square filter, the values indicates 
            the minimal and maximum RR values which are accepted
            annotation_filter (tuple): A tuple containing the flags of bbeats that need to be removed. The 0, 1, 2 and 3 flags refer to 
            sinus, ventricular, supraventricular and artifact respectively
        Returns:
            None (manipulates the annotation attribute of the Signal class)
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
        '''
        Method that creates a poincare attribute for the Signal class, making it possible to pass the Signal class attributes to the Poincare class methods.
        '''
        self.poincare = Poincare(self)

    def set_runs(self):
        '''
        Method that creates a runs attribute for the Signal class, making it possible to pass the Signal class attributes to the Runs class methods.
        '''
        self.runs = Runs(self)

    def set_LS_spectrum(self):
        '''
        Method that creates a LS_spectrum attribute for the Signal class, making it possible to pass the Signal class attributes to the LombScargleSpectrum and FFTSpectrum class methods.
        '''
        self.LS_spectrum = LombScargleSpectrum(self)

    def set_plots(self):
        '''
        Method that creates a plotRR attribute for the Signal class, making it possible to pass the Signal class attributes to the PlotRR class method.
        '''
        self.plotRR = PlotRR(self)