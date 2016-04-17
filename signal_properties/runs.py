from numpy import concatenate, delete
from scipy import diff, sign, where, array

class Runs:

    def __init__(self, signal):
        # signal is an object of the "Signal" class
        # the algorithm is the same I used in the PCSS time series suit
        self.runs_decelerations = self.get_runs(signal)[0] # get_runs returns a list of lists, with the first element being the deceleration runs
        self.runs_accelerations = self.get_runs(signal)[0]

    def get_runs(self, signal):
        pass

    def split_on_annot(self, signal):
        # this function splits the signal time series into disjoint subseries, breaking the signal on annotations which are not 0
        bad_index = where(signal.annotation != 0)[1]

        # checking if there is anything to do
        if len(bad_index) == 0:
            return(array(bad_index))

        start = 1
        signal_segments = array([])

        # now getting the actual segments of sinus origin beats (or, if you are doing something else than HRV, the "correct" elements of the time series)
        # I am sure someone can do a much better job using a more fuctional style

        