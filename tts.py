#-*-coding: utf-8-*-
#-*-coding: euc-kr-*-

import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
import pygame
import random 
from datetime import datetime

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice0.mp3'
    i = 1
    while True:
        if os.path.isfile(filename):
            os.remove(filename)
            print(f'remove {filename}')
            filename = f'voice{i}.mp3'
            i += 1
        else:
            break
    tts.save(filename)
    play_audio(filename)
    

def play_audio(filename):
    #init
    pygame.mixer.init()
    #load file
    pygame.mixer.music.load(filename)
    #play
    pygame.mixer.music.play()
    #끝까지 재생할때까지 기다린다.
    while pygame.mixer.music.get_busy() == True:
        continue

def play_misuc(music_dir):
    music_list = os.listdir(music_dir)
    music_title = music_list[random.randint(0,len(music_list)-1)]
    part, section = music_title.split('_')[:2]
    speak(f'{part}에 {section} 들려드릴께요.')
    play_audio(os.path.join('music',music_title))

def play_bible(bible_dir):
    bible_list = os.listdir('bible')
    bible_title = bible_list[random.randint(0,len(bible_list)-1)]
    part, section = bible_title.split('_')[:2]
    speak(f'오늘은 {part} {section} 읽어드릴께요')
    play_audio(os.path.join('bible',bible_title))

def play_smae(text):
    speak(f'말씀하세요. 따라 말할께요.')
    with mic as source:
        print('말씀하세요.')
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        speech_sub = r.recognize_google(audio,language='ko-KR')
        print(speech_sub)
    speak(speech_sub)
    flag = 0


r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
flag = 0
print(datetime.today().date())
exit()

while True:
    with mic as source:
        print('말씀하세요.')
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            speech = r.recognize_google(audio,language='ko-KR')
        except:
            continue
        print(speech)

    

    if flag == 1:
        if '성경' in speech:
            play_bible('bible')
            flag = 0

        elif '노래' in speech:
            play_misuc('music')
            flag = 0
            pass

        elif '성대모사' in speech:
            
            pass

        if '알람' in speech.replace(' ',''):
            speak('기상시간, 약 먹는 시간, 일회용 알람을 설정할 수 있어요. 무슨 알람을 설정하실거에요? 삐이 소리이후에 말씀해주세요.')
            speak('삐이')
            with mic as source:
                print('알람')
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                speech_call = r.recognize_google(audio,language='ko-KR')
                print(speech_call)
            if '기상' in speech_call.replace(' ',''):
                speak('네! 기상시간을 등록할께요. 몇 시로 등록할까요?')
                with mic as source:
                    print('시간')
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    speech_time= r.recognize_google(audio,language='ko-KR')
                    print(speech_time)
                for i, c in enumerate(speech_time):
                    if c == '시':
                        h = int(speech_time[:i])
                speak(f'매일 아침 {h}시에 깨워드릴께요.')
                flag = 0
                    


    else:
        if '땅콩' in speech:
            speak('네')
            flag = 1
