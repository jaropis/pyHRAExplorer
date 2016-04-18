from numpy import concatenate, delete
from scipy import mean, var, sqrt, where


class Poincare:
    def __init__(self, signal):
        # signal is object of Signal class
        self.xi, self.xii = self.filter_and_prepare(signal)
        # descriptors will be capital, functions lower case
        self.SD1 = self.sd1()
        self.SD2 = self.sd2()
        self.SDNN = self.sdnn()
        self.SD1d, self.C1d, self.SD1a, self.C1a, self.SD1I = self.short_term_asymmetry()
        self.SD2d, self.C2d, self.SD2a, self.C2a, self.SD2I = self.long_term_asymmetry()
        self.SDNNd, self.Cd, self.SDNNa, self.Ca = self.total_asymmetry()

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

    def sd1(self):
        try:
            result = sqrt(var(self.xii - self.xi)/2)
        except ZeroDivisionError:
            result = None
        return result
        # CAREFUL HERE AND BELOW!!! the definition of variance used in scipy has the denominator equal to n, NOT (n-1)!
        # this seems to be more appropriate for what we do here, so
        # if you want to get the result you would get in R or Matlab comment the line above, uncomment the lines below and go to the
        # and change the values in the test
        # n = len(self.xi)
        # try:
        #   result = sqrt(var(self.xii - self.xi)/2 * (n/(n-1)))
        #   return(result)
        # except Exception:
        #   return None

    def sd2(self):
        return(sqrt(var(self.xii + self.xi)/2))
        # CAREFUL HERE!!! the definition of variance used in scipy has the denominator equal to n, NOT (n-1)!
        # this seems to be more appropriate for what we do here, so
        # if you want to get the result you would get in R or Matlab comment the line above, uncomment the lines below and go to the
        # and change the values in the test
        #n = len(self.xii)
        #return(sqrt(var(self.xii - self.xi)/2 * (n/(n-1))))

    def sdnn(self):
        return(sqrt((self.SD1**2 + self.SD2**2)/2))
        # CAREFUL HERE!!! the definition of variance used in scipy has the denominator equal to n, NOT (n-1)!
        # this seems to be more appropriate for what we do here, so
        # if you want to get the result you would get in R or Matlab comment the line above, uncomment the lines below and go to the
        # and change the values in the test
        # n = len(self.xii)
        #
        #    SDNN = sqrt((self.SD1**2 + self.SD2**2)/2*(n/(n-1)))
        #except ZeroDivisionError:
        #    SDNN = None
        #return(SDNN)

    def short_term_asymmetry(self):
        n = len(self.xii)
        auxilary = (self.xii - self.xi) / sqrt(2)
        decelerating_indices = where(auxilary > 0)[0]
        accelerating_indices = where(auxilary < 0)[0]
        failed = False
        try:
            SD1d = sqrt(1 / n * sum(auxilary[decelerating_indices]**2))
        except ZeroDivisionError:
            failed = True
        try:
            SD1a = sqrt(1 / n * sum(auxilary[accelerating_indices]**2))
        except ZeroDivisionError:
            failed = True
        if failed:
            return None, None, None, None, None
        else:
            SD1I = sqrt(SD1d**2 + SD1a**2)
            C1d = SD1d**2/SD1I**2
            C1a = SD1a**2/SD1I**2
            return(SD1d, C1d, SD1a, C1a, SD1I)

    def long_term_asymmetry(self):
        n = len(self.xii)
        auxilary_updown = (self.xii - self.xi)

        decelerating_indices = where(auxilary_updown > 0)[0]
        accelerating_indices = where(auxilary_updown < 0)[0]
        nochange_indices = where(auxilary_updown == 0)[0]
        auxilary = (self.xii + self.xi - mean(self.xi) - mean(self.xii)) / sqrt(2)
        failed = False
        try:
            SD2d = sqrt(1/n * (sum(auxilary[decelerating_indices]**2) + 1/2 * sum(auxilary[nochange_indices]**2)))
            SD2a = sqrt(1/n * (sum(auxilary[accelerating_indices]**2) + 1/2 * sum(auxilary[nochange_indices]**2)))
        except ZeroDivisionError:
            failed = True
        if failed:
            return None, None, None, None, None
        else:
            SD2I = sqrt(SD2d**2 + SD2a**2)
            C2d = (SD2d/SD2I)**2
            C2a = (SD2a/SD2I)**2
        return(SD2d, C2d, SD2a, C2a, SD2I)

    def total_asymmetry(self):
        failed = False
        try:
            SDNNd = sqrt(1/2 * (self.SD1d**2 + self.SD2d**2))
            SDNNa = sqrt(1/2 * (self.SD1a**2 + self.SD2a**2))
            Cd = SDNNd**2 / self.SDNN**2
            Ca = SDNNa**2 / self.SDNN**2
        except TypeError:
            failed = True
        if failed:
            return None, None, None, None
        else:
            return(SDNNd, Cd, SDNNa, Ca)