from scipy import where
from my_exceptions import WrongSignal

class Runs:

    def __init__(self, signal):
        self.sinus_segments = self.split_on_annot(signal)
        self.runs = self.count_for_all(signal)
        # signal is an object of the "Signal" class
        # the algorithm is the same I used in the PCSS time series suit
        #self.runs_decelerations = self.get_runs(signal)[0] # get_runs returns a list of lists, with the first element being the deceleration runs
        #self.runs_accelerations = self.get_runs(signal)[0]

    def split_on_annot(self, signal):
        # this function splits the signal time series into disjoint subseries, breaking the signal on annotations which are not 0
        # this is necessary for the "split_segments_into_runs" function, which accepts a "clean" segment
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

    def split_segments_into_runs(self, signal_segment, all_runs = [], directions = []):
        # this function accepts a signal without annotations - this signal comes from the segmentation into "normal" (correct) beats ("samples") segments
        # it return dictionary with two keys: all_runs and directions
        # all_runs - this list keeps all the runs in order
        # directions - this list keeps the designations - thether the run in the "all_runs" list is a decelerating list (1) or an accelerating list (-1) or no_change list (0)
        if (len(signal_segment) < 2):
            raise WrongSignal
        # signal must be length 2 or more for runs to make sense
        if signal_segment[0] == signal_segment[1]:
            last = 0
        else:
            if signal_segment[0] < signal_segment[1]:
                last = 1
            else:
                last = -1
        begin = 0 # we are dropping the first sample - this is just a reference and cannot be a part of a run
        print(last)
        for index in range(1, len(signal_segment)):
            if signal_segment[index] == signal_segment[index - 1]:
                current = 0
            else:
                if signal_segment[index] > signal_segment[index - 1]:
                    current = 1
                else:
                    current = -1

            if current != last:
                if last == -1:
                    all_runs.extend([signal_segment[begin:index]])
                    directions.append("acc")
                if last == 0:
                    all_runs.extend([signal_segment[begin:index]])
                    directions.append("neutral")
                if last == 1:
                    all_runs.extend([signal_segment[begin:index]])
                    directions.append("dec")

                begin = index
                last = current
        # now check the last run
        if last == -1:
            all_runs.extend([signal_segment[begin:index + 1]])
            directions.append("acc")
        if last == 0:
            all_runs.extend([signal_segment[begin:index + 1]])
            directions.append("neutral")
        if last == 1:
            all_runs.extend([signal_segment[begin:index + 1]])
            directions.append("dec")
        return [all_runs, directions]


    def split_all_into_runs(self, signal):
        # this function splits the chunks of sinus origin (or "correct") beats (samples) into separate runs and directions of these runs
        list_of_separate_segments = self.split_on_annot(signal)
        print(list_of_separate_segments)
        separate_runs_and_directions = {"all_runs":[], "directions":[]}
        for segment in list_of_separate_segments:
            if len(segment) > 0:
                temp = self.split_segments_into_runs(segment) # see what self.split_segments_into_runs returns - it is a list with separate runs and directions
                print(temp)
                separate_runs_and_directions["all_runs"].extend(temp[0])
                separate_runs_and_directions["directions"].extend(temp[1])
        return separate_runs_and_directions

    def count_for_all(self, signal):
        # THIS IS THE MAIN FUNCTION OF THIS SOURCEFILE
        ## this functon counts all the runs of a specific type (decelerations, accelerations, no change)
        ## up to the maximum values
        ## e.g. if there is only one deceleration run of the type 1 2 3 4 5, the result will be
        ## decelerations = [0,0,0,0,1], accelerations = NULL, neutral = NULL
        split_signal = self.split_all_into_runs(signal)
        #print(split_signal)
        directions = split_signal["directions"]
        dec_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "dec"]
        # list comprehension to extract deceleration runs
        # example a = [1, 2, 1, 1]; b = ["dec", "acc", "dec", "acc"]; [a[i] for i in range(len(b)) if b[i] == "dec"; [1, 2, 1]
        acc_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "acc"] # like above
        neutral_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "neutral"]

        dec_runs_count = [len(a) for a in dec_runs]
        acc_runs_count = [len(a) for a in acc_runs]
        neutral_runs_count = [len(a) for a in neutral_runs]

        try:
            max_dec = max(dec_runs_count)
        except ValueError:
            max_dec = 0

        try:
            max_acc = max(acc_runs_count)
        except ValueError:
            max_acc = 0

        try:
            max_neutral = max(neutral_runs_count)
        except ValueError:
            max_neutral = 0

        dec_runs_all = []
        acc_runs_all = []
        neutral_runs_all = []


        for idx_dec in range(max_dec):
            dec_runs_all.extend(sum([dec_runs_count[i] for i in range(len([dec_runs_count])) if dec_runs_count[i] == idx_dec]))
        
        for idx_acc in range(max_acc):
            acc_runs_all.extend(sum([acc_runs_count[i] for i in range(len([acc_runs_count])) if acc_runs_count[i] == idx_acc]))
        
        for idx_neutral in range(max_neutral):
            neutral_runs_all.extend(sum([neutral_runs_count[i] for i in range(len([neutral_runs_count])) if neutral_runs_count[i] == idx_neutral]))

        return dec_runs_all, acc_runs_all, neutral_runs_all