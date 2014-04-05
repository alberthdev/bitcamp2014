#!/usr/bin/env python
# SoundRXTX v1.0 - receive and transmit data with sound!
# Copyright (C) 2014 Albert Huang, Neil Alberg, and William Heimsmoth
# Portions Copyright (C) 2006-2012 Hubert Pham
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import pyaudio
import wave
import numpy as np
import operator
import pprint

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30

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
max_tstep = 1

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
        tone_list = [ 800, 1000, 2000, 3000, 6000, 8000 ]
        #print "Found frequencies:"
        '''for key in sorted_fd:
            if i < 2:
                print key
                i += 1
            else:
                break'''
        '''for key in sorted_fd:
            if i < 2:
                if key[0] == 800:
                    print "BEEP - 800 Hz"
                elif key[0] == 1000:
                    print "BEEP - 1000 Hz"
                elif key[0] == 2000:
                    print "BEEP - 2000 Hz"
                elif key[0] == 3000:
                    print "BEEP - 3000 Hz"
                elif key[0] == 4000:
                    print "BEEP - 4000 Hz"
                elif key[0] == 6000:
                    print "BEEP - 6000 Hz"
                elif key[0] == 8000:
                    print "BEEP - 8000 Hz"
                elif key[0] == 9000:
                    print "BEEP - 9000 Hz"
                
                i += 1
            else:
                break
            '''
        i = 0
        for key in sorted_fd:
            if i < 4:
                i += 1
                for tone in tone_list:
                    if key[0] == tone:
                        print "BEEP - %i Hz [%i pings] [at %i]" % (key[0], key[1], i)
            else:
                break
        tstep = 0
        freq_dict = {}
    else:
        tstep += 1
 

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

#sorted_fd = sorted(freq_dict.iteritems(), key=operator.itemgetter(1))
#pprint.pprint(sorted_fd.reverse())
