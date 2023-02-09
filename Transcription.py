import numpy as np
import torch


def realtime_transcribe(manager, lang):
    while not manager.appState.empty() or not manager.recordings.empty():
        if not manager.recordings.empty():
            frames = manager.recordings.get()

            # Translating np.array holding bytes into Tensor, per OpenAI Whisper formatting
            # https://github.com/openai/whisper/discussions/450
            torch_audio = torch.from_numpy(np.frombuffer(frames, np.int16).
                                           flatten().astype(np.float32) / 32768.0)

            result = manager.model.transcribe(torch_audio, language=lang)
            manager.transcription.append(result["text"])

            # Debug printing
            print(result["text"])                       # Print each excerpt separately
            # print(" ".join(manager.transcription))      # Print each excerpt together
