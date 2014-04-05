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

import math
import struct
import pyaudio
import time

audio_rate = 48000

# Function
#     init()
#     Initialize the tone generation engine. NOT compatible with other
#     init() functions!
# No arguments
# Returns:
#     (p, stream)
#     p      - pyaudio object - necessary for other functions!
#     stream - stream object - necessary for other functions!
def init():
    audio_rate = 48000
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=audio_rate,
        output=True)
    return (p, stream)

# Function
#     end(ret)
#     Terminate the tone generation engine. NOT compatible with other
#     end() functions!
# end(
#     ret - tuple of (pyaudio_object, stream_object) returned from
#           init()
# )
# Returns: Nothing
def end(ret):
    end_indv(ret[0], ret[1])

# Function
#     end(p, stream)
#     Terminate the tone generation engine. NOT compatible with other
#     end() functions! Accepts individual object arguments.
# end(
#     p      - the pyaudio object from the tuple returned from init()
#     stream - the stream object from the tuple returned from init()
# )
# Returns: Nothing
def end_indv(p, stream):
    stream.close()
    p.terminate()

# Function
#     play_tone(frequency, amplitude, duration, audio_rate, stream)
#     Generate and play a tone given frequency, amplitude, duration,
#     and audio rate.
# play_tone(
#     frequency      - frequency to generate and play
#     amplitude      - amplitude of the tone to generate and play
#     duration       - length of time to play tone
#     audio_rate     - audio rate of the tone to generate and play
#     stream         - the stream object from the tuple returned from
#                      init()
# )
# Returns: Nothing
def play_tone(frequency, amplitude, duration, audio_rate, stream):
    N = int(audio_rate / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / audio_rate
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
    # todo: get the format from the stream; this assumes Float32
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)

'''
# play the C major scale
scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
for tone in scale:
    play_tone(tone, 0.5, 0.75, audio_rate, stream)

# up an octave
for tone in scale[1:]:
    play_tone(2*tone, 0.5, 0.75, audio_rate, stream)
'''

if __name__ == "__main__":
    (p, stream) = init()
    tone_list = [ 800, 1000, 2000, 3000, 6000, 8000 ]
    for tone in tone_list:
        print "Playing %i Hz tone!" % tone
        play_tone(tone, 1.0, 0.75, audio_rate, stream)
        time.sleep(1)



