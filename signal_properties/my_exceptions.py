class WrongSignal(Exception):
    '''
    Exception raised if the signal for runs calculations is shorter than 2
    '''
    pass

class WrongCuts(Exception):
    '''
    Exception raised if the cuts for finsing power in bands in the spectral analysis are not unique or 
    are not arranged in an increasing order.
    '''
    pass