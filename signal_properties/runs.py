from numpy import concatenate, delete
from scipy import where
from my_exceptions import WrongSignal

class Runs:

    def __init__(self, signal):
        self.sinus_segments = self.split_on_annot(signal)
        try_count = self.count_runs(self.sinus_segments[0])
        # signal is an object of the "Signal" class
        # the algorithm is the same I used in the PCSS time series suit
        #self.runs_decelerations = self.get_runs(signal)[0] # get_runs returns a list of lists, with the first element being the deceleration runs
        #self.runs_accelerations = self.get_runs(signal)[0]

    def split_on_annot(self, signal):
        # this function splits the signal time series into disjoint subseries, breaking the signal on annotations which are not 0
        # this is necessary for the "count_runs" function, which accepts a "clean" segment
        # it accepts an object of the Signal class (varname: signal)
        # it returns a list of "clean" subjects without annotations (annotations are assumed to be 0 for all of them)
        bad_indices = where(signal.annotation != 0)[0]

        # checking if there is anything to do
        if len(bad_indices) == 0:
            return([signal.signal])

        start = 0
        signal_segments = []
        for idx in bad_indices:
            end = idx
            if start < end:
                signal_segments.append(signal.signal[start:end])
            start = idx + 1
         #the last run has been rejected automatically, now let us remove the first run (we do not know where it started -- possibly before the beginning of the recording, and we do not know where the last run ended, possibly after the end of the recording)
        if signal.annotation[len(signal.signal)-1] == 0:
            signal_segments.append(signal.signal[start:len(signal.signal)])

        return signal_segments

    def count_runs(self, signal_segment, all_runs = [], directions = []):
        # this function accepts a signal without annotations - this signal comes from the segmentation into "normal" (correct) beats ("samples") segments
        # it return dictionary with two keys: all_runs and directions
        # all_runs - this list keeps all the runs in order
        # directions - this list keeps the designations - thether the run in the "all_runs" list is a decelerating list (1) or an accelerating list (-1) or no_change list (0)
        if (len(signal_segment) < 2):
            raise WrongSignal
        # signal must be length 2 or more for runs to make sense
        if signal_segment[0] == signal_segment[1]
            last = 0
        else:
            if signal_segment[0] < signal_segment[1]
                last = 1
            else:
                last = -1
        for index in range(2, (len(signal_segment)-2)):
            if signal_segment[index] == signal_segment[index + 1]:
                current = 0
            else:
                if signal_segment[index] < signal_segment[index + 1]:
                    current = 1
                else:
                    current = -1

            if current != last:
                if last == -1:
                    all_runs.append([signal_segment[begin:index]])
                    directions.append("acc")
                if last == 0:
                    all_runs.append([signal_segment[begin:index]])
                    directions.append("neutral")
                if last == 1:
                    all_runs.append([signal_segment[begin:index]])
                    directions.append("dec")

                begin = index + 1
                last = current
        # now check the last run
        if last == -1:
            all_runs.append([signal_segment[begin:index]])
            directions.append("acc")
        if last == 0:
            all_runs.append([signal_segment[begin:index]])
            directions.append("neutral")
        if last == 1:
            all_runs.append([signal_segment[begin:index]])
            directions.append("dec")
        return [all_runs, directions]


    def split_all_into_runs(self, signal):
        # this function splits the chunks of sinus origin (or "correct") beats (samples) into separate runs and directions of these runs
        list_of_separate_segments = self.split_on_annot(signal)
        separate_runs_and_directions = {"all_runs":[], "directions":[]}
        for segment in list_of_separate_segments:
            if len(segment) > 0:
                temp = self.count_runs(segment)
                separate_runs_and_directions["all_runs"].append(temp["all_runs"])
                separate_runs_and_directions["directions"].append(temp["directions"])
        return separate_runs_and_directions



