import numpy as np
import torch

def speech_recognition(manager):
    torch_audio = torch.from_numpy(np.frombuffer(manager.recording, np.int16).
                                   flatten().astype(np.float32) / 32768.0)

    result = manager.model.transcribe(torch_audio, fp16=False, language='english')
    manager.transcription = result["text"]