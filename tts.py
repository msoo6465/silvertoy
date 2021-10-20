#-*-coding: utf-8-*-
#-*-coding: euc-kr-*-
import threading

import speech_recognition as sr
from gtts import gTTS
import os
import time
import pygame
import random 
from datetime import datetime
from check_inside import video
from set_log import logger
from button_check import button
from get_info_web import get_news, get_weather

class Speaker():
    def __init__(self):
        logger.info('Speaker Start')
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=None)
        self.function_flag = 0

        self.call_time = {
            'wake_time': '',
            'drug_time': '',
            'once_time': '',
            'time_count': 3,
            'camera_time': [11, 15, 19]
        }
        self.start_speak_list = ['저는 땅콩입니다. 저에게 명령하실 때는 땅콩이라고 불러주신 후 말씀해주세요.',
                                 '안녕하세요 땅콩이에요.',
                                 '쨔쟌!!! 땅콩이가 돌아왔어요~',
                                 '저를 다시 깨워주셔서 감사해요',
                                 '땅콩이 등장!',
                                 '저는 어르신의 반려 로봇 땅콩이에요.',
                                 '다시 만나서 반가워요!',
                                 '그동안 저 보고싶으셨죠?',
                                 '저 없는동안 뭐하고 계셨어요?',
                                 '푹 자서 너무 개운해요! 저를 움직이게 해주세요.']

    def speak(self,text):
        tts = gTTS(text=text, lang='ko')
        filename = 'voice0.mp3'
        i = 1
        while True:
            if os.path.isfile(filename):
                os.remove(filename)
                filename = f'voice{i}.mp3'
                i += 1
            else:
                break
        tts.save(filename)
        self.play_audio(filename)

    def play_audio(self,filename):
        #init
        pygame.mixer.init()
        #load file
        pygame.mixer.music.load(filename)
        #play
        pygame.mixer.music.play()
        #끝까지 재생할때까지 기다린다.
        while pygame.mixer.music.get_busy() == True:
            continue

    def play_misuc(self,music_dir):
        music_list = os.listdir(music_dir)
        music_title = music_list[random.randint(0,len(music_list)-1)]
        part, section = music_title.split('_')[:2]
        self.speak(f'{part}에 {section} 들려드릴께요.')
        self.play_audio(os.path.join('music',music_title))

    def play_bible(self,bible_dir):
        bible_list = os.listdir(bible_dir)
        bible_title = bible_list[random.randint(0, len(bible_list)-1)]
        part, section = bible_title.split('_')[:2]
        self.speak(f'오늘은 {part} {section} 읽어드릴께요')
        self.play_audio(os.path.join('bible',bible_title))

    def play_same(self):
        self.speak(f'말씀하세요. 따라 말해볼께요.')
        speech_sub = self.get_text()
        self.speak(speech_sub)

    def alam(self, type):
        if type == 'wake_time':
            type_text = '기상'
        elif type == 'drug_time':
            type_text = '약먹을 '
        elif type == 'once_time':
            type_text = '일회용 알람'

        if self.call_time[type] != '':
            is_change = '변경'
        else:
            is_change = '등록'

        self.speak(f'네! {type_text}시간을 {is_change}할께요. 몇 시로 {is_change}할까요?')
        speech_time = self.get_text()
        for i, c in enumerate(speech_time):
            if c == '시':
                h = int(speech_time[:i])
        if type == 'once_time':
            self.speak(f'{h}시로 일회용 알람을 {is_change}했어요.')
        else:
            self.speak(f'매일 {h}시로 {type_text}시간을 {is_change}했어요.')
        self.call_time[type] = h
        self.function_flag = 0

    def play_climate(self):
        weather = get_weather()
        self.speak('대구 날씨 알려드릴께요.')
        self.speak(f'오늘 대구 날씨는 {weather["온도"]}도이며 {weather["상태"]}입니다. 미세먼지는 {weather["미세먼지"]}이며, 습도는 {weather["습도"]}입니다.')

    def play_news(self):
        i = 0
        news = get_news()
        self.speak('오늘의 해드라인 뉴스 3개 알려드릴께요.')
        for key, new in news.items():
            self.speak(new)
            i += 1
            if i == 3:
                break
        self.speak('입니다.')

    def check_alam(self):
        while True:
            now = datetime.now()
            if now.minute == 0:
                if str(now.hour) == self.call_time['wake_time']:
                    alam_start_time = time.time()
                    check_clicked = button(5,19)
                    check_clicked.start()
                    while True:
                        self.play_audio('effectsound/30.액션.mp3')
                        if check_clicked.get_press() == 1:
                            check_clicked.reset()
                            check_clicked.close()
                            break
                        else:
                            self.speak('일어나세요. 기상시간입니다. 종료하시려면 버튼을 눌러주세요.')
                        if time.time() - alam_start_time > 60:
                            break
                    # 기상시간 알람
                    # 알람 끄는 것 까지
                    pass
                elif str(now.hour) == self.call_time['drug_time']:
                    # 약먹는 시간 알림
                    alam_start_time = time.time()
                    while True:
                        self.play_audio('effectsound\\30.액션.mp3')
                        self.speak('약 먹을 시간이에요. 약드세요')
                        if time.time() - alam_start_time > 60:
                            break
                elif now.hour in self.call_time['camera_time']:
                    vi = video()
                    vi.start()

            elif now.minute == 50:
                if str(now.hour) == str(eval(f"{self.call_time['wake_time']}-1")):
                    alam_start_time = time.time()
                    while True:
                        self.play_audio('effectsound\\30.액션.mp3')
                        self.speak('등록된 일회용 알람 10분전입니다. 준비하세요!')
                        if time.time() - alam_start_time > 60:
                            break
            time.sleep(60)

    def get_text(self):
        with self.mic as source:
            audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
            try:
                speech = self.r.recognize_google(audio, language='ko-KR')
            except:
                return False
            return speech

    def main(self):
        self.speak(self.start_speak_list[random.randint(0,len(self.start_speak_list))])
        check_alam = threading.Thread(target=self.check_alam)
        check_alam.start()
        while True:
            speech = self.get_text()
            if not speech:
                continue
            logger.info(f'speech : {speech}')
            speech = speech.replace(' ','')
            if self.function_flag == 1:
                if time.time() - self.wait_start_time > 30:
                    self.function_flag = 0

                if '성경' in speech:
                    logger.info('play bible')
                    self.play_bible('bible')
                    self.function_flag = 0

                elif '노래' in speech:
                    logger.info('play music')
                    self.play_misuc('music')
                    self.function_flag = 0
                    pass

                elif '성대모사' in speech:
                    logger.info('play same')
                    self.play_same()
                    self.function_flag = 0
                    pass

                if '알람' in speech:
                    logger.info('alam')
                    self.speak('기상시간, 약 먹는 시간, 일회용 알람을 설정할 수 있어요. 무슨 알람을 설정하실거에요? 띠링 소리 이후에 말씀해주세요.')
                    self.play_audio('effectsound/2. 띠딩2.mp3')
                    speech_call = self.get_text()
                    speech_call = speech_call.replace(' ', '')
                    logger.info(f'speech_call : {speech_call}')

                    if '기상' in speech_call:
                        self.alam('wake_time')

                    elif '약' in speech_call:
                        self.alam('drug_time')

                    elif '일회용' in speech_call:
                        self.alam('once_time')

                    else:
                        self.speak('잘 못들었어요. 다음에 해주세요.')
                        self.function_flag = 0

                if '날씨' in speech:
                    logger.info('play weather')
                    self.play_climate()
                    self.function_flag = 0

                if '뉴스' in speech:
                    logger.info('play news')
                    self.play_news()
                    self.function_flag = 0

            if '땅콩' in speech:
                self.speak('네')
                self.wait_start_time = time.time()
                self.function_flag = 1


if __name__ == '__main__':
    speaker = Speaker()
    speaker.main()