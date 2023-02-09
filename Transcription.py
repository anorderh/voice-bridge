import time

import numpy as np
import torch


def realtime_transcribe(manager, lang):
    while manager.recording or manager.processing:
        if not manager.recordings.empty():
            frames = manager.recordings.get()

            # Translating np.array holding bytes into Tensor, per OpenAI Whisper formatting
            # https://github.com/openai/whisper/discussions/450
            np_audio = (np.frombuffer(frames, np.int16).flatten().astype(np.float32) / 32768.0)

            print(time.time())
            result = manager.model.transcribe(np_audio, language=lang)
            print(time.time())
            manager.transcription.append(result["text"])

            # Debug printing
            print(result["text"])                       # Print each excerpt separately
            # print(" ".join(manager.transcription))      # Print each excerpt together

            manager.processing = False
