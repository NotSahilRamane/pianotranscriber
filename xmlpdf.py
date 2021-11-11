import music21
import os
fileDir = "/tmp/music21/"
fileExt = ".xml"
filename = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]
print(filename[0])
filepath = fileDir + filename[0]

music21.environment.set('musicxmlPath', '/usr/bin/mscore3')

parsed = music21.converter.parse(filepath)

parsed.write('musicxml.pdf', '/mnt/d/Codes/Transcriber/output1.pdf')