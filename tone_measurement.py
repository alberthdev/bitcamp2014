#!/usr/bin/env python
# Chat Client (Test)

import sys
import soundrxtx
import thread

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

def play_tone(tone):
    soundrxtx.tone.play_tone(tone, 1, 0.5, soundrxtx.tone.audio_rate, stream)

global tone
tone = 100
#tone = 1450

if len(sys.argv) > 1:
    tone = int(sys.argv[1])

while tone < 10000:
    (pr, streamr) = soundrxtx.recognize.init()
    print "Testing tone %i!" % tone
    freq_found = False
    # recognize_live(p, stream, time_len, freq_to_detect, find_freq_func)
    thread.start_new_thread( play_tone, (tone, ) )
    soundrxtx.recognize.recognize_live(pr, streamr, 0.5, [tone, tone-50, tone-100, tone+50, tone+100], process_freq)
    if freq_found == True:
        print "  !! Found tone %i!" % tone
    soundrxtx.recognize.end((pr, streamr))
    tone += 25
