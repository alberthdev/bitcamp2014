#!/usr/bin/env python
# Chat Client (Test)

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
bit_str_buf = ""
total_bit_str = ""
freq_found = False

def process_freq(freq):
    global state
    global prev_freq
    global str_buf
    global bit_str_buf
    global total_bit_str
    global freq_found
    
    #print "FOUND FREQ: %i (Bsize: %i)" % (freq, len(bit_str_buf))
    
    if freq != prev_freq:
        if (freq == tones[0]) or (freq == tones[2]):
            freq_found = True
            if (state == 0):
                state = 1
                if (freq == tones[0]):
                    bit_str_buf += "0"
                else:
                    bit_str_buf += "1"
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
    bin_str = soundrxtx.textconvert.ASCII_to_binary(thestr)
    print "Sending binary string: %s" % bin_str
    for i in range(0, len(bin_str)):
        # play_tone(frequency, amplitude, duration, fs, stream)
        if bin_str[i] == "0":
            soundrxtx.tone.play_tone(tones[0], 1, 0.1, soundrxtx.tone.audio_rate, stream)
        else:
            soundrxtx.tone.play_tone(tones[2], 1, 0.1, soundrxtx.tone.audio_rate, stream)
        soundrxtx.tone.play_tone(tones[1], 1, 0.1, soundrxtx.tone.audio_rate, stream)

print "Initializing..."

scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
for tone in scale:
    soundrxtx.tone.play_tone(tone*2, 0.5, 0.1, soundrxtx.tone.audio_rate, stream)
for tone in scale[::-1]:
    soundrxtx.tone.play_tone(tone*2, 0.5, 0.1, soundrxtx.tone.audio_rate, stream)

tones = [1000, 3000, 6000]

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
                if bit_str_buf != '':
                    sys.stdout.write(soundrxtx.textconvert.binary_to_ASCII(bit_str_buf) + "\n")
                    sys.stdout.flush()
                    bit_str_buf = ""
                else:
                    print "No output received!"
                break
        soundrxtx.recognize.end((pr, streamr))
    elif option == 2:
        input_str = raw_input("Chat > ")
        send_str(input_str)
        
