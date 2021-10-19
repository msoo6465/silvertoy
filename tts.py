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
from dnn import video

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
    bible_list = os.listdir(bible_dir)
    bible_title = bible_list[random.randint(0, len(bible_list)-1)]
    part, section = bible_title.split('_')[:2]
    speak(f'오늘은 {part} {section} 읽어드릴께요')
    play_audio(os.path.join('bible',bible_title))

def play_same():
    speak(f'말씀하세요. 따라 말할께요.')
    with mic as source:
        print('말씀하세요.')
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        speech_sub = r.recognize_google(audio,language='ko-KR')
        print(speech_sub)
    speak(speech_sub)

def check_call():
    pass


r = sr.Recognizer()
mic = sr.Microphone(device_index=None)
flag = 0

call_time = {
    'wake_time' : '',
    'drug_time' : '',
    'once_time' : '',
    'time_count' : 3,
    'camera_time' : [11, 15, 19]
}

while True:
    with mic as source:
        print('말씀하세요.')
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            speech = r.recognize_google(audio,language='ko-KR')
        except:
            continue
        print(speech)

    speech = speech.replace(' ','')
    if flag == 1:
        if time.time() - wait_start_time > 30:
            flag = 0

        if '성경' in speech:
            play_bible('bible')
            flag = 0

        elif '노래' in speech:
            play_misuc('music')
            flag = 0
            pass

        elif '성대모사' in speech:
            play_same()
            flag = 0
            pass

        if '알람' in speech:
            speak('기상시간, 약 먹는 시간, 일회용 알람을 설정할 수 있어요. 무슨 알람을 설정하실거에요? 삐이 소리이후에 말씀해주세요.')
            play_audio('effectsound/2. 띠딩2.mp3')
            with mic as source:
                print('알람')
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                speech_call = r.recognize_google(audio,language='ko-KR')
                print(speech_call)

            if '기상' in speech_call.replace(' ',''):
                if call_time['wake_time'] != '':
                    speak('네! 기상시간을 변경할께요. 몇 시로 등록할까요?')
                    with mic as source:
                        print('기상')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time = r.recognize_google(audio, language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    speak(f'매일 아침 {h}시로 변경했어요.')
                    call_time['wake_time'] = h

                else:
                    speak('네! 기상시간을 등록할께요. 몇 시로 등록할까요?')
                    with mic as source:
                        print('기상')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time= r.recognize_google(audio,language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    speak(f'매일 아침 {h}시에 깨워드릴께요.')
                    call_time['wake_time'] = h
                flag = 0

            elif '약' in speech_call.replace(' ',''):
                if call_time['drug_time'] != '':
                    speak('네! 약먹는 시간을 변경할께요. 몇 시로 변경할까요?')
                    with mic as source:
                        print('약')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time = r.recognize_google(audio, language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    call_time['drug_time'] = h
                    speak(f'매일 {h}시로 시간을 변경했어요.')

                else:
                    speak('네! 약먹는 시간을 등록할께요. 몇 시로 등록할까요?')
                    with mic as source:
                        print('약')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time = r.recognize_google(audio, language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    call_time['drug_time'] = h
                    speak(f'매일 {h}시에 약먹는 시간 알려드릴께요.')

            elif '일회용' in speech_call.replace(' ',''):
                if call_time['once_time'] != '':
                    speak('네! 일회용 알람을 등록할께요. 몇 시로 등록할까요?')
                    with mic as source:
                        print('약')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time = r.recognize_google(audio, language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    call_time['once_time'] = h
                    speak(f'{h}시 10분 전에 알려드릴께요.')
                else:
                    speak('네! 일회용 알람을 등록할께요. 몇 시로 등록할까요?')
                    with mic as source:
                        print('약')
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                        speech_time = r.recognize_google(audio, language='ko-KR')
                        print(speech_time)
                    for i, c in enumerate(speech_time):
                        if c == '시':
                            h = int(speech_time[:i])
                    call_time['once_time'] = h
                    speak(f'{h}시 10분 전에 알려드릴께요.')
    else:
        if '땅콩' in speech:
            speak('네')
            flag = 1
            wait_start_time = time.time()

    now = datetime.now()
    if now.minute == 0:
        if str(now.hour) == call_time['wake_time']:
            alam_start_time = time.time()
            while True:
                play_audio('effectsound\\30. 액션.mp3')
                speak('일어나세요. 기상시간입니다.')
                if time.time() - alam_start_time > 60:
                    break
            # 기상시간 알람
            # 알람 끄는 것 까지
            pass
        elif str(now.hour) == call_time['drug_time']:
            # 약먹는 시간 알림
            alam_start_time = time.time()
            while True:
                play_audio('effectsound\\30. 액션.mp3')
                speak('약 먹을 시간이에요. 약드세요')
                if time.time() - alam_start_time > 60:
                    break
        elif now.hour in call_time['camera_time']:
            vi = video()
            vi.start()


    elif now.minute == 50:
        if str(now.hour) == str(eval(f"{call_time['wake_time']}-1")):
            alam_start_time = time.time()
            while True:
                play_audio('effectsound\\30. 액션.mp3')
                speak('등록된 일회용 알람 10분전입니다. 준비하세요!')
                if time.time() - alam_start_time > 60:
                    break
