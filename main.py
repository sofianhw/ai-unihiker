from unihiker import GUI
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
import openai
import numpy as np
import pyaudio
import time
import os
import sys
import json

openai.api_key = "OPENAI_API_KEY" # input OpenAI api key

# Select the language and voice (Text To Speech) for ChatGPT
voice = PiperVoice.load("models/piper/en/amy/en_US-amy-medium.onnx", "models/piper/en/amy/en_US-amy-medium.onnx.json")

# Select the language and model for Speech Recognition
model_path = "models/vosk-model-small-en-us-0.15/"
if not os.path.exists(model_path):
    print(f"Model '{model_path}' was not found. Please check the path.")
    exit(1)
model = Model(model_path)

# Initialization of PyAudio and speech recognition
p = pyaudio.PyAudio()
chunk_size=8192
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=chunk_size)
recognizer = KaldiRecognizer(model, 16000)

# change to local tts
def tts(text):
    global flag
    audio_stream = voice.synthesize_stream_raw(text)
    pTTS = pyaudio.PyAudio()
    stream = pTTS.open(format=pTTS.get_format_from_width(width=2),  # Assuming the audio is 16-bit
                    channels=1,
                    rate=22050,
                    output=True)
                    
    # Calculate the number of silence samples to prepend
    silence_duration=0.6
    silence_samples = int(silence_duration * 22050)
    silence_data = (np.zeros(silence_samples, dtype=np.int16)).tobytes()
    # Play the silence
    stream.write(silence_data)                    
    print("Playing audio")
    # Play the stream chunk by chunk
    for audio_bytes in audio_stream:
        stream.write(audio_bytes)

    stream.stop_stream()
    stream.close()
    pTTS.terminate()
    print("Playing audio done")
    u_gui.stop_thread(thread1)
    flag = 0


# openai
def askOpenAI(question):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages = question
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# text display
def text_update():
    global y1
    time.sleep(16)
    while True:
        y1 -= 2
        time.sleep(0.15)
        trans.config(y = y1)

# event callback function
def button_click1():
    global flag
    flag = 1
    

def button_click2():
    global flag
    flag = 3

def button_click3():
    global flag
    flag = 0

u_gui=GUI()
# GUI
print("Render GUI")
img1=u_gui.draw_image(image="assets/background.jpg",x=0,y=0,w=240)
button=u_gui.draw_image(image="assets/mic.jpg",x=13,y=240,h=60,onclick=button_click1)
refresh=u_gui.draw_image(image="assets/refresh.jpg",x=157,y=240,h=60,onclick=button_click2)
init=u_gui.draw_text(text="Tap to speak",x=27,y=50,font_size=15, color="#00CCCC")
trans=u_gui.draw_text(text="",x=5,y=0, color="#000000", w=230)
back=u_gui.draw_image(image="assets/backk.jpg",x=0,y=268,onclick=button_click3)
DigitalTime=u_gui.draw_digit(text=time.strftime("%Y/%m/%d       %H:%M"),x=9,y=5,font_size=12, color="black")


result = ""
flag = 0 # 0: idle, 1: recording, 2: thinking, 3: reset
text_display = ""
y1 = 0

message = [{"role": "system", "content": "You are a helpful assistant. always reply short."}]
user = {"role": "user", "content": ""}
assistant = {"role": "assistant", "content": ""}

# Threshold setting, the specific value needs to be adjusted according to the actual situation
THRESHOLD = 20  # Assuming this is the detected silence threshold
SILENCE_DURATION = 2  # 2 seconds silent time

# Recording control variables
is_recording = 0
print("Starting Program")
while True:
    if (flag == 0):
        button.config(image="assets/mic.jpg",state="normal")
        refresh.config(image="assets/refresh.jpg",state="normal")
        back.config(image="",state="disable")
        DigitalTime.config(text=time.strftime("%Y/%m/%d       %H:%M"))
        
    data = stream.read(chunk_size)
    if recognizer.AcceptWaveform(data):
        result_json = json.loads(recognizer.Result())
        text = result_json.get('text', '')
        if text:
            print("\r" + text, end='\n')
            last_sound_time = time.time()

            if flag == 2:
                print("recording")
                trans.config(text=text)
                stream.stop_stream()

                DigitalTime.config(text=time.strftime(""))
                trans.config(text="Thinking。。。")
                user["content"] = text
                message.append(user.copy())
                openai_resp = askOpenAI(message)
                assistant["content"] = openai_resp
                message.append(assistant.copy())
                trans.config(text=openai_resp)
                back.config(image="assets/backk.jpg",state="normal")

                thread1=u_gui.start_thread(text_update)
                tts(openai_resp)
                stream.start_stream()

                while not (flag == 0):
                    pass

                y1 = 0
                trans.config(text="      ", y = y1)
                button.config(image="",state="normal")
                refresh.config(image="",state="normal")
                init.config(x=15)
                
                continue

    else:
        partial_json = json.loads(recognizer.PartialResult())
        partial = partial_json.get('partial', '')
        sys.stdout.write('\r' + partial)
        sys.stdout.flush()    

    if (flag == 3):
        message.clear()
        message = [{"role": "system", "content": "You are a helpful assistant. always reply short."}]

    if (flag == 1):
        print("listening")
        DigitalTime.config(text=time.strftime(""))
        is_recording = 1
        init.config(x=600)
        trans.config(text="Listening。。。")
        stream.start_stream()
        button.config(image="",state="disable")
        refresh.config(image="",state="disable")
        back.config(image="",state="disable")

        flag = 2