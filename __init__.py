# Developed by: jcasoft
#               Juan Carlos Argueta
# Now migrated, tested and working in Python3

from mycroft.configuration import ConfigurationManager
from adapt.intent import IntentBuilder
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context

from mycroft.skills.audioservice import AudioService
from mycroft.audio import wait_while_speaking

import os
import time
from os.path import dirname, join
from mutagen.mp3 import MP3

from mtranslate import translate


__author__ = 'jcasoft'


class TranslateSkill(MycroftSkill):

    def __init__(self):
        super(TranslateSkill, self).__init__('TranslateSkill')
        self.language = self.lang
        self.process = None
        self.path_translated_file = "/tmp/translated.mp3"

    def initialize(self):
        self.tts = ConfigurationManager.get().get("tts").get("module")
        self.audioservice = AudioService(self.emitter)

        intent = IntentBuilder('HowUseIntent')\
            .require('HowUseKeyword') \
            .require('SkillNameKeyword') \
            .build()
        self.register_intent(intent, self.handle_how_use)

    @intent_handler(IntentBuilder("TranslateIntent").require("TranslateKeyword")
                    .require('ToKeyword')
                    .require('LanguageNameKeyword')
                    .require('phrase')
                    .build())
    @adds_context("TranslateContext")
    def handle_translate_intent(self, message):
        word = message.data.get("TranslateKeyword")
        lang = message.data.get("LanguageNameKeyword")
        sentence = message.data.get("phrase")
        translated = translate(sentence, lang)
        self.say(translated, lang)

    @intent_handler(IntentBuilder("TranslateToIntent")
                    .require("TranslateKeyword")
                    .require('ToKeyword')
                    .require('translate')
                    .require('LanguageNameKeyword')
                    .build())
    @adds_context("TranslateContext")
    def handle_translate_to_intent(self, message):
        lang = message.data.get("LanguageNameKeyword")
        sentence = message.data.get("translate")
        to = message.data.get("ToKeyword")
        translated = translate(sentence, lang)
        self.say(translated, lang)

    @intent_handler(IntentBuilder("RepeatTranslate") .require(
        'RepeatKeyword').require("TranslateContext").build())
    def handle_repeat_translate(self, message):
        self.emitter.emit(Message('recognizer_loop:mute_mic'))
        self.emitter.emit(Message('recognizer_loop:audio_output_start'))
        time.sleep(1)

        wait_while_speaking()
        self.audioservice.play(self.path_translated_file)  

        self.emitter.emit(Message('recognizer_loop:unmute_mic'))
        self.emitter.emit(Message('recognizer_loop:audio_output_end'))

    @intent_handler(IntentBuilder("OthersLanguagesIntent")
                    .require("SpeakKeyword")
                    .require("LanguageKeyword")
                    .build())
    @adds_context("OthersLanguagesContext")
    def handle_others_languages(self, message):
        data = None
        self.speak_dialog("yes.ask", data, expect_response=True)

    @intent_handler(IntentBuilder("OtherLanguageTranslateIntent").require(
        "OthersLanguagesContext").build())
    def handle_other_language_translate(self, message):
        resp = message.data.get("utterance")


        langs = [
            "en|english",
            "es|spanish",
            "it|italian",
            "fr|french",
            "nl|dutch",
            "de|german",
            "pl|polish",
            "pt|portuguese",
            "da|danish",
            "hu|hungarian",
            "sv|swedish",
            "no|norwegian",
            "ca|catalan",
            "ro|romanian",
            "sk|slovak",
            "zh-TW|chinese",
            "ja|japanese"]

        language = self.language

        self.emitter.emit(Message('recognizer_loop:mute_mic'))
        i = 0
        for i in range(0, len(langs)):
            lang = langs[i].split("|")
            lang = lang[0]
            if lang == language:
                print("*****Skip language.....")
            else:
                translated = translate(resp, lang)
                self.say(translated, lang)
                audio_file = MP3(self.path_translated_file)
                time.sleep(audio_file.info.length+1.5)

            i = i + 1

        self.speak_dialog("what.did.you.think")


    def handle_how_use(self, message):
        self.speak_dialog("how.use")

    def say(self, sentence, lang):
        self.enclosure.deactivate_mouth_events()
        get_sentence = 'wget -q -U Mozilla -O /tmp/translated.mp3 "https://translate.google.com/translate_tts?ie=UTF-8&tl=' + \
            str(lang) + '&q=' + str(sentence) + '&client=tw-ob' + '"'

        os.system(get_sentence)
        self.enclosure.mouth_text(sentence)

        wait_while_speaking()
        self.audioservice.play(self.path_translated_file)      

        audio_file = MP3(self.path_translated_file)
        time.sleep(audio_file.info.length)


        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()

    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('translate.stop')
            self.process.terminate()
            self.process.wait()




def create_skill():
    return TranslateSkill()
