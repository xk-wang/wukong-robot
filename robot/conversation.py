# -*- coding: utf-8-*-
from robot import ASR, TTS, AI, Player, config, constants, utils
from snowboy import snowboydecoder
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Conversation(object):

    def __init__(self):
        self.player = None
        self.asr = ASR.get_engine_by_slug(config.get('asr_engine', 'tencent-asr'))
        self.ai = AI.get_robot_by_slug(config.get('robot', 'tuling'))
        self.tts = TTS.get_engine_by_slug(config.get('tts_engine', 'baidu-tts'))

    def converse(self, fp):
        try:
            self.interrupt()
            snowboydecoder.play_audio_file(constants.getData('beep_lo.wav'))
            query = self.asr.transcribe(fp)
            utils.check_and_delete(fp)
            msg = self.ai.chat(query)        
            self.say(msg)
        except ValueError as e:
            logger.critical(e)
            utils.clean()

    def say(self, msg):
        voice = self.tts.get_speech(msg)
        self.player = Player.SoxPlayer()
        self.player.play(voice, True)

    def interrupt(self):
        if self.player is not None and self.player.is_playing():
            self.player.stop()
            self.player = None