import numpy as np
import torch

def speech_recognition(manager):
    while not manager.appState.empty():     # appState, for thread communication
        if not manager.recordings.empty():      # Recordings present to be transcribed
            audio_bytes = manager.recordings.get()
            torch_audio = torch.from_numpy(np.frombuffer(audio_bytes, np.int16).flatten().astype(np.float32) / 32768.0)

            result = manager.model.transcribe(torch_audio, fp16=False, language='english')
            print("-> " + result["text"])
            manager.msg += result["text"]