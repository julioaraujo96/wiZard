#!/usr/bin/env python3

from time import sleep
from vosk import Model, KaldiRecognizer
from pywizlight import wizlight, PilotBuilder, discovery
import pyaudio
import pyttsx3
import json
import asyncio

# Síntese de fala
engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[-1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

light = wizlight('192.168.1.71');

#ligar
async def turn_on():
    await light.turn_on()
    await asyncio.sleep(3)

#desligar
async def turn_off():
    await light.turn_off()
    await asyncio.sleep(3)

# Reconhecimento de voz
model = Model('model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

async def listen():
    active = True;
    while active:
        print('Giovanna, a ouvir...');
        data = stream.read(2048)
        if len(data) == 0:
            break;
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)
            if result is not None:
                text = result['text'] 
                print(text);
                if "ligar" in text: 
                    speak('A ligar as luzes');
                    await turn_on();
                    sleep(3);
                if "apagar" in text: 
                    speak('A apagar as luzes');
                    await turn_off();
                if "sair" in text:
                    active = False;

async def main():
# Loop do reconhecimento de voz
    while True:
        print('Fala Giovanna, para ativar o assistente...');
        data = stream.read(2048)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)
            if result is not None:
                text = result['text'] 
                if "giovanna" in text:
                    speak('Bem vinda, sou a giovanna, em que posso ajudar?') 
                    await listen();
                print('Text: {}'.format(text))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())