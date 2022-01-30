import numpy as np
import os
import tensorflow.compat.v1 as tf
print("1")
# from google.colab import files

from tensor2tensor import models
print("2")
from tensor2tensor import problems
print("3")
from tensor2tensor.data_generators import text_encoder
print("4")
from tensor2tensor.utils import decoding
print("5")
from tensor2tensor.utils import trainer_lib
print("6")
from magenta.models.score2perf import score2perf
print("7")
import note_seq
print("8")

tf.disable_v2_behavior()

SF2_PATH = '/content/Yamaha-C5-Salamander-JNv5.1.sf2'
SAMPLE_RATE = 16000

# Upload a MIDI file and convert to NoteSequence.
def upload_midi():
  data = list(files.upload().values())
  if len(data) > 1:
    print('Multiple files uploaded; using only one.')
  return note_seq.midi_to_note_sequence(data[0])

# Decode a list of IDs.
def decode(ids, encoder):
  ids = list(ids)
  if text_encoder.EOS_ID in ids:
    ids = ids[:ids.index(text_encoder.EOS_ID)]
  return encoder.decode(ids)

model_name = 'transformer'
hparams_set = 'transformer_tpu'
ckpt_path = 'gs://magentadata/models/music_transformer/checkpoints/melody_conditioned_model_16.ckpt'

class MelodyToPianoPerformanceProblem(score2perf.AbsoluteMelody2PerfProblem):
  @property
  def add_eos_symbol(self):
    return True

problem = MelodyToPianoPerformanceProblem()
melody_conditioned_encoders = problem.get_feature_encoders()

# Set up HParams.
hparams = trainer_lib.create_hparams(hparams_set=hparams_set)
trainer_lib.add_problem_hparams(hparams, problem)
hparams.num_hidden_layers = 16
hparams.sampling_method = 'random'

# Set up decoding HParams.
decode_hparams = decoding.decode_hparams()
decode_hparams.alpha = 0.0
decode_hparams.beam_size = 1

# Create Estimator.
run_config = trainer_lib.create_run_config(hparams)
estimator = trainer_lib.create_estimator(
    model_name, hparams, run_config,
    decode_hparams=decode_hparams)

# These values will be changed by the following cell.
inputs = []
decode_length = 0

# Create input generator.
def input_generator():
  global inputs
  while True:
    yield {
        'inputs': np.array([[inputs]], dtype=np.int32),
        'targets': np.zeros([1, 0], dtype=np.int32),
        'decode_length': np.array(decode_length, dtype=np.int32)
    }
print("______________________START ESTIMATOR_____________________")
# Start the Estimator, loading from the specified checkpoint.
input_fn = decoding.make_input_fn_from_generator(input_generator())
melody_conditioned_samples = estimator.predict(
    input_fn, checkpoint_path=ckpt_path)
print("______________________END ESTIMATOR_____________________")
# "Burn" one.
_ = next(melody_conditioned_samples)
print("______________________END SOMETHING_____________________")

melody = 'Upload your own!' 

if melody == 'Upload your own!':
  # Extract melody from user-uploaded MIDI file.
  print("______________________WAITING FOR FILES_____________________")
  melody_ns = upload_midi()
  print("______________________GOT FOR FILES_____________________")
  melody_instrument = note_seq.infer_melody_for_sequence(melody_ns)
  notes = [note for note in melody_ns.notes
           if note.instrument == melody_instrument]
  del melody_ns.notes[:]
  melody_ns.notes.extend(
      sorted(notes, key=lambda note: note.start_time))
  for i in range(len(melody_ns.notes) - 1):
    melody_ns.notes[i].end_time = melody_ns.notes[i + 1].start_time
  inputs = melody_conditioned_encoders['inputs'].encode_note_sequence(
      melody_ns)
else:
  # Use one of the provided melodies.
  events = [event + 12 if event != note_seq.MELODY_NO_EVENT else event
            for e in melodies[melody]
            for event in [e] + event_padding]
  inputs = melody_conditioned_encoders['inputs'].encode(
      ' '.join(str(e) for e in events))
  melody_ns = note_seq.Melody(events).to_sequence(qpm=150)

# Play and plot the melody.
note_seq.play_sequence(
    melody_ns,
    synth=note_seq.fluidsynth, sample_rate=SAMPLE_RATE, sf2_path=SF2_PATH)
note_seq.plot_sequence(melody_ns)

# Generate sample events.
decode_length = 4096
sample_ids = next(melody_conditioned_samples)['outputs']

# Decode to NoteSequence.
midi_filename = decode(
    sample_ids,
    encoder=melody_conditioned_encoders['targets'])
accompaniment_ns = note_seq.midi_file_to_note_sequence(midi_filename)

# Play and plot.
note_seq.play_sequence(
    accompaniment_ns,
    synth=note_seq.fluidsynth, sample_rate=SAMPLE_RATE, sf2_path=SF2_PATH)
note_seq.plot_sequence(accompaniment_ns)