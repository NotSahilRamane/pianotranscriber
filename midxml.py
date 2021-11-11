import os
import glob
import music21

files = glob.glob('/tmp/music21/*')
for f in files:
    os.remove(f)

parsed = music21.converter.parse('output.mid')
parsed.write()