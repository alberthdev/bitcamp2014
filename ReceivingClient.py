import pyaudio
import wave
import numpy as np
import operator
import binascii
import pprint

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
#RATE = 44100
RATE = 44100
RECORD_SECONDS = 10

# use a Blackman window
window = np.blackman(CHUNK)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

freq_dict = {}

swidth = p.get_sample_size(FORMAT)

tstep = 0
max_tstep = 0

output = 0

# play stream and find the frequency of each CHUNK
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/CHUNK
        #print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which*RATE/CHUNK
        #print "The freq is %f Hz." % (thefreq)
    
    rthefreq = int(round(thefreq/5.0)*5.0)
    if rthefreq in freq_dict:
        freq_dict[rthefreq] += 1
    else:
        freq_dict[rthefreq] = 1
    
    if tstep == max_tstep:
        sorted_fd = sorted(freq_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
        i = 0
        #print "Found frequencies:"
        '''for key in sorted_fd:
            if i < 2:
                print key
                i += 1
            else:
                break'''
        for key in sorted_fd:
            if i < 2:
                if key[0] == 1000:
                    output += '0'
                elif key[0] == 5000:
                    output += '1'
                i += 1
            else:
                break
        tstep = 0
        freq_dict = {}
    else:
        tstep += 1
 

print("* done recording")

print(binascii.unhexlify('%x' % output))

stream.stop_stream()
stream.close()
p.terminate()

#sorted_fd = sorted(freq_dict.iteritems(), key=operator.itemgetter(1))
#pprint.pprint(sorted_fd.reverse())
