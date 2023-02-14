# ![voicebridge logo](assets/voicebridge.png)

*A speech-to-speech translation desktop app powered by Whisper and Google Translate*

![GitHub last commit](https://img.shields.io/github/last-commit/anorderh/voice-bridge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/anorderh/voice-bridge)
![GitHub contributors](https://img.shields.io/github/contributors/anorderh/voice-bridge)
![GitHub](https://img.shields.io/github/license/anorderh/voice-bridge)

![video](assets/demo.mp4)

## Goal

This repo's goal was to develop an appliction testing Whisper's capabilities for real-time voice transcription. Implementing [SpeechRecognizers](https://github.com/Uberi/speech_recognition) made this possible by processing audio input per lingual pauses. 

## Usage

1. Run the executable `voicebridge`.
2. Select your *input* and *output* languages.
3. Generate `.mp3` files of translated speech.
4. Save and replay up to <u>7 different recordings at a time</u>.

## Requirements

- OpenAI Whisper
- deep_translator
- speech_recognition
- gTTs
- tkinter

## Limitations

Voicebridge requires an internet connection due to Google API use.

- To implement offline functionality, look into [Argos Translate](https://github.com/argosopentech/argos-translate) and [pyttsx3](https://github.com/nateshmbhat/pyttsx3)

## Contributing

Pull requests are welcomed. For major changes, please open an issue first to discuss what you would like to change. 
