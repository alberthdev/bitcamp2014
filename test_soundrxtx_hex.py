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

import sys
import soundrxtx

(p, stream) = soundrxtx.tone.init()

global state
global prev_freq
global str_buf
global bit_str_buf
global total_bit_str
global freq_found
state = 0
prev_freq = 0
str_buf = ""
base_str_buf = ""
total_bit_str = ""
freq_found = False

def process_freq(freq):
    global state
    global prev_freq
    global str_buf
    global base_str_buf
    global total_bit_str
    global freq_found
    
    if freq != prev_freq:
        for tone in tones:
            if tone == freq:
                freq_found = True
                print "FOUND FREQ: %i (Bsize: %i)" % (freq, len(base_str_buf))
                if (freq != tones[-1]):
                    if (state == 0):
                        state = 1
                        base_str_buf += soundrxtx.textconvert.base_letters[tones.index(freq)]
                    else:
                        print "WARNING: Extra tone found in wrong state!"
                else:
                    if (state == 1):
                        state = 0
                    else:
                        print "WARNING: Blank tone found in wrong state!"
    prev_freq = freq
    
    '''if (len(bit_str_buf) % 8 == 0) and (len(bit_str_buf) != 0):
        sys.stdout.write(soundrxtx.textconvert.binary_to_ASCII(bit_str_buf))
        sys.stdout.flush()
        total_bit_str += bit_str_buf
        print "bits: %s" % bit_str_buf
        bit_str_buf = ""'''

def send_str(thestr):
    bin_str = soundrxtx.textconvert.ASCII_to_hex(thestr)
    print "Sending hex string: %s" % bin_str
    for i in range(0, len(bin_str)):
        # play_tone(frequency, amplitude, duration, fs, stream)
        print tones[soundrxtx.textconvert.base_letters.index(bin_str[i])]
        soundrxtx.tone.play_tone(tones[soundrxtx.textconvert.base_letters.index(bin_str[i])], 1, 0.1, soundrxtx.tone.audio_rate, stream)
        soundrxtx.tone.play_tone(tones[-1], 1, 0.1, soundrxtx.tone.audio_rate, stream)

print "Initializing..."

scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
for tone in scale:
    soundrxtx.tone.play_tone(tone*2, 0.5, 0.1, soundrxtx.tone.audio_rate, stream)
for tone in scale[::-1]:
    soundrxtx.tone.play_tone(tone*2, 0.5, 0.1, soundrxtx.tone.audio_rate, stream)

# NEED:  17
#        1    2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17
tones = [500, 550,  600,  750,  800,  1000, 1200, 1500, 1600, 2000, 2400, 3000, 3200, 4800, 6000, 8000, 9600]

while True:
    print "Options:"
    print " 1) Receive"
    print " 2) Transmit"
    option = int(raw_input("> "))
    
    if option == 1:
        (pr, streamr) = soundrxtx.recognize.init()
        for i in range(0, 60):
            freq_found = False
            # recognize_live(p, stream, time_len, freq_to_detect, find_freq_func)
            soundrxtx.recognize.recognize_live(pr, streamr, 5, tones, process_freq)
            if not freq_found:
                if base_str_buf != '':
                    if len(base_str_buf) % 2 == 0:
                        sys.stdout.write(soundrxtx.textconvert.hex_to_ASCII(base_str_buf) + "\n")
                        sys.stdout.flush()
                    else:
                        print "Data corruption detected, please try again!"
                    base_str_buf = ""
                else:
                    print "No output received!"
                break
        soundrxtx.recognize.end((pr, streamr))
    elif option == 2:
        input_str = raw_input("Chat > ")
        send_str(input_str)
        
