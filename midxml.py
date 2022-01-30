import os
import glob
import music21

def midTOXML():
    files = glob.glob('/tmp/music21/*')
    for f in files:
        os.remove(f)

    parsed = music21.converter.parse('output.mid')
    parsed.write()
    print("DONE MIDXML")