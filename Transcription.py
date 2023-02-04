import numpy as np
import torch

def speech_recognition(model, audio_bytes):
    torch_audio = torch.from_numpy(np.frombuffer(audio_bytes, np.int16).flatten().astype(np.float32) / 32768.0)

    result = model.transcribe(torch_audio, fp16=False, language='english')
    print(f"OpenAI Whisper: \n" + result["text"])