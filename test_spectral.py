import scipy
import scipy.signal as sc
import matplotlib.pyplot as plt
from signal_properties.RRclasses import Signal
from signal_properties.my_exceptions import WrongCuts


A1 = 8.
omega1 = 1        
nin = 11
x = scipy.linspace(0.01, 2*scipy.pi, nin)
y1 = A1 * scipy.sin(omega1*(x))
signal3 = Signal([y1, scipy.absolute(y1*0), x])
signal3.set_LS_spectrum()
signal3.LS_spectrum.periodogram = scipy.linspace(0.0, 1.0, nin) * 0 + 1.0/(nin-1)
signal3.LS_spectrum.frequency = scipy.linspace(0.0, 1.0, nin)

cuts = [0.0, 0.5, 1]
#signal3.LS_spectrum.get_bands(cuts, 1) == scipy.array([0.5, 0.5])).all())
#print(signal3.LS_spectrum.get_bands(cuts, 1))
#print()

#prints [0,0] instead of [0.5, 0,5] so the first assertions from spectral_test returns false

A1 = 8.
A2 = 2.
omega1 = 1
omega2 = 2
nin = 1000
x = scipy.linspace(0.01, 2*scipy.pi, nin)
y1 = A1 * scipy.sin(omega1*(x))
y2 = A2 * scipy.sin(omega2*(x))
y = y1+y2
signal5 = Signal([y, scipy.absolute(y*0), x])
signal5.set_LS_spectrum()
signal51 = Signal([y1, scipy.absolute(y*0), x])
signal51.set_LS_spectrum()
signal52 = Signal([y2, scipy.absolute(y*0), x])
signal52.set_LS_spectrum()
variance = scipy.var(y)
variance1 = scipy.var(y1)
variance2 = scipy.var(y2)
df = (signal5.LS_spectrum.frequency[1] -  signal5.LS_spectrum.frequency[0])
#print(df)
spectral_content = signal5.LS_spectrum.get_bands(cuts=[0.2, 2.0], df=df)
# this should be equal to the variance of the whole signal - the peaks are quite broad here, so wide integration interval
spectral_content1 = signal51.LS_spectrum.get_bands(cuts=[0.2, 2.0], df=df)
spectral_content2 = signal52.LS_spectrum.get_bands(cuts=[0.2, 2.5], df=df)
#print(spectral_content[0], variance)
#print(spectral_content1[0], variance1)
#print(spectral_content2[0], variance2)

#variance in all spectral content is = 0
#print(signal5.LS_spectrum.get_bands(cuts = [1.0, 2.0], df = df))


cuts=[0.2, 2.0]


first = cuts[0]
power_in_bands = []
for second in cuts[1:]:
    # no interpolation since the frequencies are closely spaced in self.frequency (see the build_spectrum method)
    first_index = scipy.where(signal5.LS_spectrum.frequency >= first)[0]
    second_index = scipy.where(signal5.LS_spectrum.frequency >= second)[0]
    #print(first_index, second_index, signal5.LS_spectrum.frequency[0])
    print('first_index:', first_index[0], 'second index:', second_index[0], 'freq:', signal5.LS_spectrum.frequency[0])
    print('len first:', len(first_index), 'len second:', len(second_index))
    if first_index[0] == second_index[0]:
        # here, if there is no power in the first band, and there is some in the following one,
        # this condition must hold
        power_in_bands.append(0.0)
        first = second # go to the next band
    elif len(second_index > 0): # if there is any power in the band above the current band
        power_in_bands.append(sum(signal5.LS_spectrum.periodogram[first_index[0]:second_index[0]]))
        first = second
    elif len(first_index) >= 1: # so, there is no power in the band above - is there any power
        power_in_bands.append(sum(signal5.LS_spectrum.periodogram[first_index[0]:first_index[-1]]))
        break
    else:
        break
#print("dupa", power_in_bands * df) returned TypeError: can't multiply sequence by non-int of type 'numpy.float64' changed format to prevent the error
print(power_in_bands)
print('sum', sum(signal5.LS_spectrum.periodogram[first_index[0]:second_index[0]]))
print(first_index[-1], second_index[0])

print('variance', variance, 'bands', [i * df for i in power_in_bands])
#return scipy.array(power_in_bands) * df returned TypeError: can't multiply sequence by non-int of type 'numpy.float64'
#print(scipy.array([i * df for i in power_in_bands]))

frequency = scipy.linspace(0.01, 2*scipy.pi, len(signal5.LS_spectrum.filtered_time_track))
        # here the assumption is that the frequencies are below 1Hz
        # which obviously may not be true
periodogram = sc.lombscargle(signal5.LS_spectrum.filtered_time_track, signal5.LS_spectrum.filtered_signal, frequency) / len(signal5.LS_spectrum.filtered_time_track) * 4 * signal5.LS_spectrum.filtered_time_track[len(signal5.LS_spectrum.filtered_time_track)-1] / (2*scipy.pi) / 2

#print(frequency)
#print(periodogram)

#print(signal5.LS_spectrum.periodogram[first_index[0]:first_index[-1]])
#signal5.LS_spectrum.first_index[-1] = 999 signal5.LS_spectrum.second_index[0] = 317
# as 999>317, the returned periodogram and its sum is empty
#as a result power_in_bands is empty as well
#print(signal5.LS_spectrum.periodogram[999:317])
#print( len(signal5.LS_spectrum.filtered_time_track))
#print(signal5.LS_spectrum.filtered_time_track)

#print(first_index)
