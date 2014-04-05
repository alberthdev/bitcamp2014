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

global rec_running
rec_running = False

# use a Blackman window
window = np.blackman(CHUNK)

# Function
#     init()
#     Initialize the recognition engine. NOT compatible with other
#     init() functions!
# No arguments
# Returns:
#     (p, stream)
#     p      - pyaudio object - necessary for other functions!
#     stream - stream object - necessary for other functions!
def init():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return (p, stream)

# Function
#     end(ret)
#     Terminate the recognition engine. NOT compatible with other end()
#     functions!
# end(
#     ret - tuple of (pyaudio_object, stream_object) returned from
#           init()
# )
# Returns: Nothing
def end(ret):
    end_indv(ret[0], ret[1])

# Function
#     end(p, stream)
#     Terminate the recognition engine. NOT compatible with other end()
#     functions! Accepts individual object arguments.
# end(
#     p      - the pyaudio object from the tuple returned from init()
#     stream - the stream object from the tuple returned from init()
# )
# Returns: Nothing
def end_indv(p, stream):
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function
#     recognize_live(p, stream, time_len, freq_to_detect, find_freq_func)
#     Recognize given frequencies from audio and call a function when
#     a frequency is detected.
# recognize_live(
#     p              - pyaudio object (from init())
#     stream         - input audio pyaudio.Stream() object (from init())
#     time_len       - length of time to record
#                      Set this to 0 for infinite recording
#     freq_to_detect - array of frequencies to detect
#     find_freq_func - function callback when a frequency is found.
#                      Function should have these arguments:
#                      def my_callback_func(freq)
# )
# Returns: Nothing
def recognize_live(p, stream, time_len, freq_to_detect, find_freq_func):
    global rec_running
    rec_running = True
    frames = []

    freq_dict = {}

    swidth = p.get_sample_size(FORMAT)

    tstep = 0
    max_tstep = 1
    
    if time_len == 0:
        time_len = 100000 # hacky, but it'll work for now
    
    # play stream and find the frequency of each CHUNK
    for i in range(0, int(RATE / CHUNK * time_len)):
        if not rec_running:
            break
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
        else:
            thefreq = which*RATE/CHUNK
        
        rthefreq = int(round(thefreq/5.0)*5.0)
        if rthefreq in freq_dict:
            freq_dict[rthefreq] += 1
        else:
            freq_dict[rthefreq] = 1
        
        if tstep == max_tstep:
            sorted_fd = sorted(freq_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
            tone_list = freq_to_detect
            i = 0
            for key in sorted_fd:
                if i < 4:
                    i += 1
                    for tone in tone_list:
                        if key[0] == tone:
                            find_freq_func(key[0])
                else:
                    break
            tstep = 0
            freq_dict = {}
        else:
            tstep += 1
    rec_running = False

# Function
#     recognize(p, stream, time_len, freq_to_detect, find_freq_func)
#     Recognize given frequencies from audio and call a function when
#     a frequency is detected.
# recognize(
#     p              - pyaudio object (from init())
#     stream         - input audio pyaudio.Stream() object (from init())
#     time_len       - length of time to record
#                      Set this to 0 for infinite recording
#     freq_to_detect - array of frequencies to detect
# )
# Returns:
#     freq_array - array of frequencies found, in order of time found
def recognize(p, stream, time_len, freq_to_detect):
    global rec_running
    rec_running = True

    frames = []

    freq_dict = {}

    swidth = p.get_sample_size(FORMAT)

    tstep = 0
    max_tstep = 1
    
    freq_array = []
    
    if time_len == 0:
        time_len = 100000 # hacky, but it'll work for now
    
    # play stream and find the frequency of each CHUNK
    for i in range(0, int(RATE / CHUNK * time_len)):
        if not rec_running:
            break
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
        else:
            thefreq = which*RATE/CHUNK
        
        rthefreq = int(round(thefreq/5.0)*5.0)
        if rthefreq in freq_dict:
            freq_dict[rthefreq] += 1
        else:
            freq_dict[rthefreq] = 1
        
        if tstep == max_tstep:
            sorted_fd = sorted(freq_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
            tone_list = freq_to_detect
            i = 0
            for key in sorted_fd:
                if i < 4:
                    i += 1
                    for tone in tone_list:
                        if key[0] == tone:
                            freq_array.append(key[0])
                else:
                    break
            tstep = 0
            freq_dict = {}
        else:
            tstep += 1
    
    rec_running = False
    
    # Return!
    return freq_array

# Function
#     kill()
#     Kill the currently running recognition.
# No arguments.
# Returns:
#     kill_success - True if kill was successful, False if not.
def kill():
    global rec_running
    
    if rec_running:
        rec_running = False
        return True
    else:
        return False
