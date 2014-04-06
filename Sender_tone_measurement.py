#!/usr/bin/env python
# Chat Client (Test)

import sys
import soundrxtx
import thread
import time

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

def play_tone(tone):
    soundrxtx.tone.play_tone(tone, 1, 0.5, soundrxtx.tone.audio_rate, stream)

global tone
tone = 100
#tone = 1450

while tone < 10000:
    print "Testing tone %i!" % tone
    thread.start_new_thread( play_tone, (tone, ) )
    time.sleep(0.5)
    tone += 25
