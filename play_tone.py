import math
import struct
import pyaudio
import time

audio_rate = 48000

def init():
    audio_rate = 48000
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=audio_rate,
        output=True)
    return (p, stream)

def end(ret):
    end_indv(ret[0], ret[1])

def end_indv(p, stream):
    stream.close()
    p.terminate()

def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
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
    play_tone(tone, 0.5, 0.75, fs, stream)

# up an octave
for tone in scale[1:]:
    play_tone(2*tone, 0.5, 0.75, fs, stream)
'''

if __name__ == "__main__":
    (p, stream) = init()
    tone_list = [ 800, 1000, 2000, 3000, 6000, 8000 ]
    for tone in tone_list:
        print "Playing %i Hz tone!" % tone
        play_tone(tone, 1.0, 0.75, audio_rate, stream)
        time.sleep(1)



