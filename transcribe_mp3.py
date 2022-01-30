from inference import Transcriber
from config import sample_rate
from utilities import load_audio
import torch

def transcribe(mp3_file):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("Using ", device, "for processing")

    transcriber = Transcriber(device=device)

    audio, _ = load_audio(mp3_file, sr=sample_rate, mono=True)

    transcribed_dict = transcriber.transcribe(audio, 'output.mid')
