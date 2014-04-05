soundtxrx (SoundLoad R&D Project)
==================================
*A Bitcamp 2014 Project*

Usage:  
```python
import soundrxtx
# (p, stream) = soundrxtx.tone.init()
# soundrxtx.tone.end((p, stream))
# soundrxtx.tone.end_indv(p, stream)
# soundrxtx.tone.play_tone(frequency, amplitude, duration, audio_rate, stream)

# (p, stream) = soundrxtx.recognize.init()
# soundrxtx.recognize.end((p, stream))
# soundrxtx.recognize.end_indv(p, stream)
# soundrxtx.recognize.recognize_live(p, stream, 10, [1000, 2000], myfunc)
# soundrxtx.recognize.recognize(p, stream, 10, [1000, 2000])
# soundrxtx.recognize.kill()
```
