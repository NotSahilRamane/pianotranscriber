import note_seq
from midi2audio import FluidSynth

FluidSynth().midi_to_audio('output.mid', 'output.wav')
# SF2_PATH = 'Yamaha-C5-Salamander-JNv5.1.sf2'
# SAMPLE_RATE = 16000
# in_file = open("output.mid", "rb") # opening for [r]eading as [b]inary
# data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
# in_file.close()
# melody_ns = note_seq.midi_to_note_sequence(data)
# melody_instrument = note_seq.infer_melody_for_sequence(melody_ns)
# notes = [note for note in melody_ns.notes
#         if note.instrument == melody_instrument]
# del melody_ns.notes[:]
# melody_ns.notes.extend(
#     sorted(notes, key=lambda note: note.start_time))
# for i in range(len(melody_ns.notes) - 1):
#     melody_ns.notes[i].end_time = melody_ns.notes[i + 1].start_time
# # Play and plot the melody.
# # note_seq.play_sequence(
# #     melody_ns,
# #     synth=note_seq.fluidsynth, sample_rate=SAMPLE_RATE)