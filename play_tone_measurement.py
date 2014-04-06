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
    
    #if freq != prev_freq:
    #    print "FOUND FREQ: %i (Bsize: %i)" % (freq, len(bit_str_buf))
    prev_freq = freq
    
    if freq == tone:
        freq_found = True
    
    '''if (len(bit_str_buf) % 8 == 0) and (len(bit_str_buf) != 0):
        sys.stdout.write(soundrxtx.textconvert.binary_to_ASCII(bit_str_buf))
        sys.stdout.flush()
        total_bit_str += bit_str_buf
        print "bits: %s" % bit_str_buf
        bit_str_buf = ""'''

global tone
tone = 100
#tone = 1450
while tone < 10000:
    sys.stderr.write("Playing tone %i!\n" % tone)
    try:
        (p, stream) = soundrxtx.tone.init()
        soundrxtx.tone.play_tone(tone, 1, 0.5, soundrxtx.tone.audio_rate, stream)
        soundrxtx.tone.end((p, stream))
    except KeyboardInterrupt:
        break
    except:
        print "CRASH! Stopped at %i." % tone
    tone += 50
