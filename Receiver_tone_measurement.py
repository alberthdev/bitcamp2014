'''
Created on Apr 6, 2014

@author: William Heimsoth
'''
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
    
    prev_freq = freq
    
    if freq == tone:
        freq_found = True

global tone
tone = 100
#tone = 1450

while tone < 10000:
    (pr, streamr) = soundrxtx.recognize.init()
    print "Testing tone %i!" % tone
    freq_found = False
    soundrxtx.recognize.recognize_live(pr, streamr, 0.5, [tone, tone-50, tone-100, tone+50, tone+100], process_freq)
    if freq_found == True:
        print "  !! Found tone %i!" % tone
    soundrxtx.recognize.end((pr, streamr))
    tone += 25
