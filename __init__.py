# Developed by: jcasoft
#               Juan Carlos Argueta
# Now migrated, tested and working in Python3

from adapt.intent import IntentBuilder
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context
from mycroft.util import play_mp3

import os
import time

from mtranslate import translate


__author__ = 'jcasoft'


class TranslateSkill(MycroftSkill):

    def __init__(self):
        super(TranslateSkill, self).__init__('TranslateSkill')
        self.language = self.lang

    def initialize(self):

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

        p = play_mp3("/tmp/translated.mp3")
        p.communicate()

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
                #self.speak_dialog("in",{'language': langs[i].split("|")[1]})
                #time.sleep(1.8)
                self.enclosure.deactivate_mouth_events()
                translated = translate(resp, lang)
                self.enclosure.mouth_text(translated)
                self.say(translated, lang)

            i = i + 1

        mycroft.audio.wait_while_speaking()
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()

        self.speak_dialog("what.did.you.think")
        self.emitter.emit(Message('recognizer_loop:unmute_mic'))
        self.emitter.emit(Message('recognizer_loop:audio_output_end'))

    def handle_how_use(self, message):
        self.speak_dialog("how.use")

    def say(self, sentence, lang):
        self.emitter.emit(Message('recognizer_loop:mute_mic'))

        get_sentence = 'wget -q -U Mozilla -O /tmp/translated.mp3 "https://translate.google.com/translate_tts?ie=UTF-8&tl=' + \
            str(lang) + '&q=' + str(sentence) + '&client=tw-ob' + '"'

        os.system(get_sentence)

        self.emitter.emit(Message('enclosure.mouth.text'))
        p = play_mp3("/tmp/translated.mp3")
        p.communicate()

        time.sleep(0.2)
        self.emitter.emit(Message('recognizer_loop:unmute_mic'))


def create_skill():
    return TranslateSkill()
