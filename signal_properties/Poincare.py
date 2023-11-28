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
        ND (float): (PI = Porta's index) the contribution of the number of HR decelerations to all normal heartbeats.
        pNN50 (float): Proportion of consecutive RR intervals of normal (sinus) orign that differ by more than 50ms
        pNN_neutral (float): Proportion of consecutive RR intervals of normal (sinus) orign that are the same
        SD2_SD1 (float): The ratio of SD2 to SD1 that measures the balance between the long- and short-term HRV
        CS (float): Stores the value of the contribution of the short-term variance to the total HRV
        CSa (float): Stores the value of the contribution of the short-term variance to the total HRV derived from HR accelerations
        CSd (float): Stores the value of the contribution of the short-term variance to the total HRV derived from HR decelerations
        CLa (float): Stores the value of the contribution of the long-term variance to the total HRV derived from HR accelerations
        CLd (float): Stores the value of the contribution of the long-term variance to the total HRV derived from HR decelerations
        HRA1 (int): Presence of short-term HRA, either 1 or 0
        HRA2 (int): Presence of long-term HRA, either 1 or 0
        HRAT (int): Presence of total HRA, either 1 or 0
        HRAN (int): Presence of fewer HR decelerations than accelerations, either 1 or 0
        HRAcomp (int): HRA compensation, either 1 or 0

    Args:
        signal (Signal): Contains information about the RR signal, such as RR values, annotation and timetrack.
    '''
    def __init__(self, signal):

        # signal is object of Signal class
        self.xi, self.xii = self.prepare_PP(signal)
        self.filtered_time = self.filter_time(signal)
        # descriptors will be capital, methods lower case
        self.SD1 = self.sd1()
        self.SD2 = self.sd2()
        self.SDNN, self.SD2_SD1 = self.sd2_sd1()
        self.meanRR = self.meanrr()
        self.CV = self.cv()
        # pNNn
        self.pNN50 = self.pnnx()[0]
        self.pNN_neutral = self.pnn_neutral()
        # HRA
        self.SD1d, self.C1d, self.SD1a, self.C1a, self.SD1I, self.ND = self.short_term_asymmetry()
        self.SD2d, self.C2d, self.SD2a, self.C2a, self.SD2I = self.long_term_asymmetry()
        self.SDNNd, self.Cd, self.SDNNa, self.Ca = self.total_asymmetry()
        self.HRA1, self.HRA2, self.HRAT, self.HRAN, self.HRAcomp = self.hra_forms()
        # HRV
        self.CS, self.CSa, self.CSd = self.short_term_variability()
        self.CLa, self.CLd = self.long_term_variability()
        

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
        Method that filteres the time, removing the times corresponding to the beats deleted from the signal
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

    def sd2_sd1(self):
        '''
        Calculates the SDNN parameter for the signal using the xi and xii attributes of class Poincare.

        Returns:
            SDNN (float): The value of the square root of the total RR intervals variance (SDNN)
            SD2/SD1 (float): The ratio of SD2 to SD1 that measures the balance between the long- and short-term HRV
        '''
        try:
            SDNN = sqrt((self.SD1**2 + self.SD2**2)/2)
            SD2_SD1 = self.SD2 / self.SD1
        except ZeroDivisionError:
            SD2_SD1 = None
        return(SDNN, SD2_SD1)
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
            meanRR = mean(self.xi)
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
    
    def pnnx(self, x = 50):
        '''
        Calculates the pNN based on the differences between consequtive RR intervals (xi and xii)

        Args:
            x (int): The desired difference between the RR intervals, default 50

        Returns:
            pNNX (float): Proportion of consecutive RR intervals of normal (sinus) orign that differ by more than X ms
            pNNX_d (float): Proportion of consecutive RR intervals of normal (sinus) orign that differ by more than X ms and decelerate 
            pNNX_a (float): Proportion of consecutive RR intervals of normal (sinus) orign that differ by more than X ms and accelerate
        '''
        differences = self.xii - self.xi
        if x < 0:
            print('Invalid x value')
            return None, None, None
        else: 
            pnnX_d = 100*len(where(differences > x)[0])/len(self.xi)
            pnnX_a = 100*len(where(differences < -1*x)[0])/len(self.xi)
            pnnX = pnnX_d + pnnX_a
            return pnnX, pnnX_d, pnnX_a

    def pnn_pro(self, x = 5):
        '''
        Calculates the pNN% based on the changes between consequtive RR intervals (xi and xii)

        Args:
            x (int): The desired procentage change between the RR intervals, default 5%

        Returns:
            pNNX (float): Proportion of consecutive RR intervals of normal (sinus) orign that are changed by more than X% compared to the previous beat
            pNNX_d (float): Proportion of consecutive RR intervals of normal (sinus) orign that are increased by X% or more compared to the previous beat
            pNNX_a (float): Proportion of consecutive RR intervals of normal (sinus) orign that are decreased by X% or more compared to the previous beat
        '''
        changes = 100*self.xii/self.xi
        if x < 0:
            print('Invalid x value')
            return None, None, None
        else: 
            pnnX_d_pro = 100*len(where(changes - 100 > x)[0])/len(self.xi)
            pnnX_a_pro = 100*len(where(100 - changes > x)[0])/len(self.xi)
            pnnX_pro = pnnX_d_pro + pnnX_a_pro
            return pnnX_pro, pnnX_d_pro, pnnX_a_pro
        
    def pnn_neutral(self):
        differences = self.xii - self.xi
        pnn_nu = 100*len(where(differences == 0)[0])/len(self.xi)
        
        return pnn_nu
    
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
            ND (float): (PI = Porta's index) the contribution of the number of HR decelerations to all normal heartbeats.
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
            return None, None, None, None, None, None
        else:
            SD1I = sqrt(SD1d**2 + SD1a**2)
            C1d = SD1d**2/SD1I**2
            C1a = SD1a**2/SD1I**2
            Nd = len(decelerating_indices)/(len(decelerating_indices) + (len(accelerating_indices)))
            return(SD1d, C1d, SD1a, C1a, SD1I, Nd)

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
        
    def hra_forms(self):
        '''
        Determines the presence of different types of HRA based on contributions of decelerations to different forms of HRV

        Returns:
            HRA1 (int): Presence of short-term HRA, either 1 or 0
            HRA2 (int): Presence of long-term HRA, either 1 or 0
            HRAT (int): Presence of total HRA, either 1 or 0
            HRAN (int): Presence of fewer HR decelerations than accelerations, either 1 or 0
            HRAcomp (int): HRA compensation, either 1 or 0
        '''
        failed = False
        try:
            hra1 = 1 if self.C1d > 0.5 else 0
            hra2 = 1 if self.C2d < 0.5 else 0
            hrat = 1 if self.Cd < 0.5 else 0
            hran = 1 if self.ND < 0.5 else 0
            hracomp = 1 if (hra1 + hra2) == 2 else 0
        except TypeError:
            failed = True
        if failed:
            return None, None, None, None, None
        else:
            return(hra1, hra2, hrat, hran, hracomp)
        
    def short_term_variability(self):
        '''
        Calculates and returns the short-term HRV parameters, using the SD1, SD1a, SD1d and SDNN attributes of class Poincare

        Returns:
            CS (float): Stores the value of the contribution of the short-term variance to the total HRV
            CSa (float): Stores the value of the contribution of the short-term variance to the total HRV derived from HR accelerations
            CSd (float): Stores the value of the contribution of the short-term variance to the total HRV derived from HR decelerations
        '''
        failed = False
        try:
            Cs = self.SD1**2/(2*self.SDNN**2)
            Csa = self.SD1a**2/(2*self.SDNN**2)
            Csd = self.SD1d**2/(2*self.SDNN**2)
        except TypeError:
            failed = True
        if failed:
            return None, None, None
        else:
            return(Cs, Csa, Csd)
        
    def long_term_variability(self):
        '''
        Calculates and returns the long-term HRV parameters, using the SD2a, SD2d and SDNN attributes of class Poincare  

        Returns:
            CLa (float): Stores the value of the contribution of the long-term variance to the total HRV derived from HR accelerations
            CLd (float): Stores the value of the contribution of the long-term variance to the total HRV derived from HR decelerations
        '''
        failed = False
        try:
            Cla = self.SD2a**2/(2*self.SDNN**2)
            Cld = self.SD2d**2/(2*self.SDNN**2)
        except TypeError:
            failed = True
        if failed:
            return None, None
        else:
            return(Cla, Cld)

