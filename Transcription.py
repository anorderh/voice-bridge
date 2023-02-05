import numpy as np
import torch

def speech_recognition(manager, to_code):
    # Translating np.array holding bytes into Tensor, per OpenAI Whisper formatting
    # https://github.com/openai/whisper/discussions/450
    torch_audio = torch.from_numpy(np.frombuffer(manager.recording, np.int16).
                                   flatten().astype(np.float32) / 32768.0)

    result = manager.model.transcribe(torch_audio, fp16=False, language=to_code) #FP16 for CPU processing
    manager.transcription = result["text"]