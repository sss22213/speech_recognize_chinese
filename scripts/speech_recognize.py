#!/usr/bin/env python3

import speech_recognition
import jieba
import jieba.posseg as pseg
from pypinyin import pinyin, lazy_pinyin, Style

class speech_recognize_status:
    wait_for_trigger = 0
    wait_for_recognize = 1


class speech_recognize:
    def __init__(self, pass_word, language="zh-TW"):
        self.speech_recognize_engine = speech_recognition.Recognizer()
        self.pass_word = lazy_pinyin(pass_word)
        self.language = language
        self.status_flag = speech_recognize_status().wait_for_trigger

    def recognize(self):
        # listening from microphone
        with speech_recognition.Microphone() as source:
            audio = self.speech_recognize_engine.listen(source)

        try:
            text = self.speech_recognize_engine.recognize_google(audio, language=self.language)
        except:
            return None

        # recognize
        return text

    def command_analysis_engine(self):
        recognize_word = self.recognize()
        if recognize_word == None:
            return "", [], [], []

        words = pseg.cut(recognize_word)
        norn = []
        verb = []
        m = []
        total_text = []
        for word, flag in words:
            total_text.append(word)
            if flag == 'n' or  flag == 'r':
                norn.append(word)
            elif flag == 'v':
                verb.append(word)
            elif flag == 'm':
                m.append(word)
        return total_text, norn, verb, m

    def run_conversion(self):
        total_text, norn, verb, m = self.command_analysis_engine()
        self.status_flag = speech_recognize_status().wait_for_trigger
        pass

    def run_forever(self):
        while True:
            total_text, norn, verb, m = self.command_analysis_engine()
            print(total_text)
            if lazy_pinyin(total_text) == self.pass_word:
                self.status_flag = speech_recognize_status().wait_for_recognize

            if self.status_flag == speech_recognize_status().wait_for_recognize:
                # Process command
                self.run_conversion()
            elif self.status_flag == speech_recognize_status().wait_for_trigger:
                # Waiting for keyword
                continue
        pass


if __name__ == '__main__':
    '''
    ok ['ok']
    柏宏 ['bai', 'hong']
    '''
    sr = speech_recognize(pass_word = 'ok柏宏')
    sr.run_forever()

        