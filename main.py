from inference import Transcriber
from config import sample_rate
from utilities import load_audio
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using ", device, "for processing")

transcriber = Transcriber(device=device)

audio, _ = load_audio('elise.mp3', sr=sample_rate, mono=True)

transcribed_dict = transcriber.transcribe(audio, 'output.mid')
