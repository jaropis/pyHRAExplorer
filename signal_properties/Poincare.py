from numpy import concatenate, delete, mean, var, sqrt, where


class Poincare:
    '''
    Poincare class used to calculate and store descriptors of HRV and prepere vectors needed for a Poincare plot.

    Attributes:
        xi (array): An array containting the filtered RRn signal values
        xii (array): An array containting the filtered RRn+1 signal values
        filtered_time (array): An array containting the filtered values of timetrack (corresponding to xi)
        SD1 (float): Stores the value of the square root of the short-term RR intervals variance
        SD2 (float): Stores the value of the square root of the long-term RR intervals variance
        SDNN (float): Stores the value of the square root of the total RR intervals variance
        SD1d (float): Stores the value of the square root of the short-term RR intervals variance derived from decelerations
        C1d (float): Stores the value of the contribution of HR decelerations to the short-term HRV
        SD1a (float): Stores the value of the square root of the short-term RR intervals variance derived from accelerations
        C1a (float): Stores the value of the contribution of HR accelerations to the short-term HRV
        SD1I (float): Stores the value of the square root of the sum of short-term RR variance from accelerations and decelerations
        SD2d (float): Stores the value of the square root of the long-term RR intervals variance derived from decelerations
        C2d (float): Stores the value of the contribution of HR decelerations in long-term HRV
        SD2a (float): Stores the value of the square root of the long-term RR intervals variance derived from accelerations
        C2a (float): Stores the value of the contribution of HR accelerations in long-term HRV
        SD2I (float): Stores the value of the square root of the sum of long-term RR variance from accelerations and decelerations
        SDNNd (float): Stores the value of the square root of the total RR intervals variance derived from decelerations
        Cd (float): Stores the value of the contribution of HR decelerations in total HRV
        SDNNa (float): Stores the value of the square root of the total RR intervals variance derived from accelerations
        Ca (float): Stores the value of the contribution of HR accelerations in total HRV
        meanRR (float): Stores the value of mean RR signal after filtering
        CV (float): Stores the value of the index of total variance normalized to the mean RR


    Args:
        signal (Signal): Contains information about the RR signal, such as RR values, annotation and timetrack.
    '''
    def __init__(self, signal):

        # signal is object of Signal class
        self.xi, self.xii = self.prepare_PP(signal)
        self.filtered_time = self.filter_time(signal)
        # descriptors will be capital, functions lower case
        self.SD1 = self.sd1()
        self.SD2 = self.sd2()
        self.SDNN = self.sdnn()
        self.SD1d, self.C1d, self.SD1a, self.C1a, self.SD1I = self.short_term_asymmetry()
        self.SD2d, self.C2d, self.SD2a, self.C2a, self.SD2I = self.long_term_asymmetry()
        self.SDNNd, self.Cd, self.SDNNa, self.Ca = self.total_asymmetry()
        self.meanRR = self.meanrr()
        self.CV = self.cv()

    def prepare_PP(self, signal):
        """
        This method prepares the auxiliary vectors for Poincare Plot, the filtering method follows 
        "Filtering Poincare plots", Piskorski, Guzik, Computational methods in science and technology 11 (1), 39-48

        Args:
            signal (Signal): Here Signal class property signal (array) which contains values of RR reads will be used 
            alongside the Signal class  property annotation (array) which marks the beats that should be removed with '16'

        Returns:
            xi (array): An array containting the filtered RRn signal values
            xii (array): An array containting the filtered RRn+1 signal values

        """
        # the signal has already been filtered in the constructor of the Signal class - i.e. all places which should
        # be removed were marked in signal.annotation as 16

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
    
    def filter_time(self,signal):
        '''
        Function that filteres the time, removing the times corresponding to the beats deleted from the signal
        (for example ventricular, supraventricular or artifact beats). 

        Args:
            signal (Signal): 

        Returns:
            filtered_time (array): An array containting the filtered values of timetrack

        '''
        #Adding filtered time for tachygraph
        filtered_time = signal.timetrack[1:len(signal.timetrack)]
        bad_beats = where(signal.annotation == 16)[0]
        bad_beats_minus_one = bad_beats - 1
        all_bad_beats = concatenate((bad_beats, bad_beats_minus_one))
        filtered_time = delete(filtered_time, all_bad_beats)

        return filtered_time


    def sd1(self):
        '''
        Calculates the SD1 parameter for the signal using the xi and xii attributes of class Poincare.

        Returns:
            result (float): The value of the square root of the short-term RR intervals variance (SD1)
        '''
        try:
            result = sqrt(var(self.xii - self.xi)/2)
        except ZeroDivisionError:
            result = None
        return result
        # CAREFUL HERE AND BELOW!!! the definition of variance used in numpy has the denominator equal to n, NOT (n-1)!
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
        '''
        Calculates the SD2 parameter for the signal using the xi and xii attributes of class Poincare.

        Returns:
            result (float): The value of the square root of the long-term RR intervals variance (SD2)
        '''

        return(sqrt(var(self.xii + self.xi)/2))
        # CAREFUL HERE!!! the definition of variance used in numpy has the denominator equal to n, NOT (n-1)!
        # this seems to be more appropriate for what we do here, so
        # if you want to get the result you would get in R or Matlab comment the line above, uncomment the lines below and go to the
        # and change the values in the test
        #n = len(self.xii)
        #return(sqrt(var(self.xii - self.xi)/2 * (n/(n-1))))

    def sdnn(self):
        '''
        Calculates the SDNN parameter for the signal using the xi and xii attributes of class Poincare.

        Returns:
            result (float): The value of the square root of the total RR intervals variance (SDNN)
        '''
        return(sqrt((self.SD1**2 + self.SD2**2)/2))
        # CAREFUL HERE!!! the definition of variance used in numpy has the denominator equal to n, NOT (n-1)!
        # this seems to be more appropriate for what we do here, so
        # if you want to get the result you would get in R or Matlab comment the line above, uncomment the lines below and go to the
        # and change the values in the test
        # n = len(self.xii)
        #
        #    SDNN = sqrt((self.SD1**2 + self.SD2**2)/2*(n/(n-1)))
        #except ZeroDivisionError:
        #    SDNN = None
        #return(SDNN)

    def meanrr(self):
        '''
        Calculates the mean RR interval for the signal using the xi and xii attributes of class Poincare.

        Returns:
            meanRR (float): The value of mean RR signal after filtering
        '''
        try:
            meanRR = mean(self.xii)
        except ZeroDivisionError:
            meanRR = None
        return(meanRR)
    
    def cv(self):
        '''
        Calculates the CV parameter for the signal using the xi and xii attributes of class Poincare.

        Returns:
            CV (float): The value of index of total variance normalized to the mean RR
        '''    
        # calculate CV after filtering for RRn
        meanRR = self.meanRR 
        SDNN = self.SDNN
        try:
            CV = SDNN/meanRR
        except ZeroDivisionError:
            CV = None
        return CV

    def short_term_asymmetry(self):
        '''
        Calculates the short-term asymmetry parameters for the signal using the xi and xii attributes of class Poincare, 
        finds the decelerating and accelerating indeces to derive their individual short-term RR interval variance and contributions to 
        short-term HRV

        Returns:
            SD1d (float): The value of the square root of the short-term RR intervals variance derived from decelerations
            C1d (float): The value of the contribution of HR decelerations to the short-term HRV
            SD1a (float): The value of the square root of the short-term RR intervals variance derived from accelerations
            C1a (float): The value of the contribution of HR accelerations to the short-term HRV
            SD1I (float): The value of the square root of the sum of short-term RR variance from accelerations and decelerations
        '''
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
        '''
        Calculates the long-term asymmetry parameters for the signal using the xi and xii attributes of class Poincare, 
        finds the decelerating and accelerating indeces to derive their individual long-term RR interval variance and contributions to 
        long-term HRV

        Returns:
            SD2d (float): The value of the square root of the long-term RR intervals variance derived from decelerations
            C2d (float): The value of the contribution of HR decelerations in long-term HRV
            SD2a (float): The value of the square root of the long-term RR intervals variance derived from accelerations
            C2a (float): The value of the contribution of HR accelerations in long-term HRV
            SD2I (float): The value of the square root of the sum of long-term RR variance from accelerations and decelerations
        '''
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
        '''
        Calculates the total asymmetry parameters for the signal using the SD1d and SD2d attributes of class Poincare  

        Returns:
            SDNNd (float): The value of the square root of the total RR intervals variance derived from decelerations
            Cd (float): The value of the contribution of HR decelerations in total HRV
            SDNNa (float): The value of the square root of the total RR intervals variance derived from accelerations
            Ca (float): The value of the contribution of HR accelerations in total HRV
        '''
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