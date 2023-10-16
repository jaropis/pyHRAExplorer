from numpy import where
from signal_properties.my_exceptions import WrongSignal


class Runs:
    '''
    Runs class that splits the signal into segments and runs, counting the number of accelerations, decelerations and neutral runs

    Attributes:
        runs (tuple): A tuple containg all the lists with summary of the number and type of the decelerated, accelerated or neutral runs.
        dec_runs (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for decelerations
	    acc_runs (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for accelerations
	    neutral_runs (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for neutral 
    '''
    def __init__(self, signal):
        '''
        Initializes the attributes of the Signal class, passing arguments to methods.

        Args:
            signal (Signal): Object of class signal, its signal and annotation properties will be used to find the types and counts of the RR signal runs
        '''
        # self.sinus_segments = self.split_on_annot(signal) # - uncomment here and in tests
        self.runs = self.count_for_all(signal)
        self.dec_runs, self.acc_runs, self.neutral_runs = self.count_for_all(signal)
        #self.dec_runs_share, self.acc_runs_share, self.neutral_runs_share = self.count_for_all_share(signal)
        #self.test = self.count_for_all_share(signal)
        # the algorithm is the same I used in the PCSS time series suit

    def split_on_annot(self, signal):
        '''
        This method splits the signal time series into disjoint subseries, breaking the signal on annotations which are not 0
        this is necessary for the "split_segments_into_runs" function, which accepts a "clean" segment
        
        Args: 
            signal (Signal): Here Signal class attribute signal (array) and Signal class attribute annotation (array) will be used to find the sinus beats and separate them into runs

        Returns:
            signal_segments(list): List of "clean" subjects without annotations (annotations are assumed to be 0 for all of them)
        '''

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
            #  the last run has been rejected automatically, now let us remove the
            #  first run (we do not know where it started -- possibly before the beginning of the recording,
            #  and we do not know where the last run ended, possibly after the end of the recording)
        if signal.annotation[len(signal.signal)-1] == 0:
            signal_segments.append(signal.signal[start:len(signal.signal)])

        return signal_segments

    def split_segments_into_runs(self, signal_segment, all_runs = [], directions = []):
        '''
        This method accepts a signal without annotations, which has already been split into the "normal" (correct) beats ("samples") segments by the split_on_annot() method     
        
        Args:
            signal_segment (list): List of "clean" subjects without annotations (annotations are assumed to be 0 for all of them)
            all_runs (list): creates an empty list
            directions (list): creates an empty list
            
        Returns:
            A dictionary containing two keys:
            ['all_runs'] which contains the list with all the runs in order
            ['directions'] which contains a list keeps the directions of the runs in the "all_runs", indicating if the runs is a decelerating list (1) 
            or an accelerating list (-1) or no_change list (0)
        '''
        # 
        # it return dictionary with two keys: all_runs and directions
        # all_runs - this list keeps all the runs in order
        # directions - this list keeps the designations - thether the run in the "all_runs"
        #  list is a decelerating list (1) or an accelerating list (-1) or no_change list (0)
        if (len(signal_segment) < 2): # the length of the signal must be sufficient
            raise WrongSignal
        if signal_segment[0] == signal_segment[1]:
            last = 0
        else:
            if signal_segment[0] < signal_segment[1]:
                last = 1
            else:
                last = -1
        begin = 1 # we are dropping the first sample - this is just a reference and cannot be a part of a run - this
        # could happen either after the beginning of a signal or after an "incorrect" (e.g. extrasystolic) sample
        # well, perhaps the run after the beginning or after the incorrect beat should be rejected altogether ...
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
        '''
        This method splits the chunks of sinus origin beats into separate runs and directions (acceleration/deceleration/neutral) of these runs
        
        Args:
	        signal (Signal): Here Signal class attribute signal (array) and Signal class attribute annotation (array) will be used to find the sinus beats and separate them into runs
        
        Returns:
	        separate_runs_and_directions (dict): A dictionary with two keys: ['all_runs'] which contain the lists of consequtive runs of a given type and ['directions'] with types of runs (acc/dec/neutral)
        '''
        # this function splits the chunks of sinus origin (or "correct") beats
        #  (samples) into separate runs and directions of these runs
        list_of_separate_segments = self.split_on_annot(signal)
        separate_runs_and_directions = {"all_runs":[], "directions":[]}
        for segment in list_of_separate_segments:
            if len(segment) > 0:
                temp = self.split_segments_into_runs(segment, all_runs=[], directions=[])
                # see what self.split_segments_into_runs returns - it is a list with separate runs and directions
                separate_runs_and_directions["all_runs"].extend(temp[0])
                separate_runs_and_directions["directions"].extend(temp[1])
        return separate_runs_and_directions

    def count_for_all(self, signal):
        '''
        Counts how many times a run of a given type (acceleration, deceleration, neutral) and length occurs in the signal

        Args:
	        signal (Signal): Here Signal class property signal (array) will be used to find the acceleration, deceleration or neutral runs and count the number of times a run of a given length and type shows up 
        
        Returns:
	        dec_runs_all (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for decelerations
	        acc_runs_all (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for accelerations
	        neutral_runs_all (list): A list of counts of runs in length ranging from 1 to the maximum length of the run for neutral 
        '''
        if (len(signal.signal) < 2):
            raise WrongSignal
        # THIS IS THE MAIN FUNCTION OF THIS SOURCEFILE
        # this functon counts all the runs of a specific type (decelerations, accelerations, no change)
        # up to the maximum values
        # e.g. if there is only one deceleration run of the type 1 2 3 4 5, the result will be
        # decelerations = [0,0,0,0,1], accelerations = NULL, neutral = NULL
        split_signal = self.split_all_into_runs(signal)
        directions = split_signal["directions"]
        dec_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "dec"]
        # list comprehension to extract deceleration runs
        # example a = [1, 2, 1, 1]; b = ["dec", "acc", "dec", "acc"]; [a[i] for i in range(len(b)) if b[i] == "dec"; [1, 2, 1]
        acc_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "acc"] # like above
        neutral_runs = [split_signal["all_runs"][i] for i in range(len(directions)) if directions[i] == "neutral"]

        # these variables are lists of lengths of runs, so if dec runs is [[1,2], [1,2,3]] then the dec_runs_count
        # will be [2, 3]
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

        dec_runs_all = [0] * max_dec
        acc_runs_all = [0] * max_acc
        neutral_runs_all = [0] * max_neutral

        for idx_dec in range(1, max_dec + 1):
            # basically, return 1 if a given deceleration run in dec_runs_count is of idx_dec length and then sum
            # the ones, in this way the deceleration runs of length idx_dec will be counted
            for i in range(len(dec_runs_count)):
                if dec_runs_count[i] == idx_dec:
                    dec_runs_all[idx_dec-1] += 1 # necessary to address the list element correctly
        
        for idx_acc in range(1, max_acc + 1):
            for i in range(len(acc_runs_count)):
                if acc_runs_count[i] == idx_acc:
                    acc_runs_all[idx_acc-1] += 1

        for idx_neutral in range(1, max_neutral + 1):
            for i in range(len(neutral_runs_count)):
                    if neutral_runs_count[i] == idx_neutral:
                        neutral_runs_all[idx_neutral - 1] += 1

        return dec_runs_all, acc_runs_all, neutral_runs_all
    
    def count_for_all_share(self, signal):
        run_count = self.count_for_all(signal)
        split_signal = self.split_all_into_runs(signal)
        runs = split_signal["all_runs"]
        n = 0
        for run in runs:
            n = n + len(run)
        
        try: 
            1/n
        except ZeroDivisionError:
            count_all_share = None

        count_all_share = []
        for direction in run_count:
            for i in range(1, len(direction) + 1):
                direction[i-1] = round(100*(direction[i-1]*i)/n, 2)
            count_all_share.append(direction)

        return count_all_share



