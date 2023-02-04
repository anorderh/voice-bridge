def speech_recognition(model, audio):
    result = model.transcribe(audio, language='english')
    print(f"OpenAI Whisper: \n {result['text']}")