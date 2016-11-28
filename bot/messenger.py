# -*- coding: utf-8 -*-

import logging
import random
import re
import weather_manager
from resource_manager import ResourceManager
from pkmn_manager import PokemonManager

SASS_FLAG = re.compile('sass[a-z]* ')
logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.help_manager = ResourceManager('help_text.txt')
        self.pkmn_manager = PokemonManager()
        self.blame_manager = ResourceManager('blames.txt')
        self.explanation_manager = ResourceManager('explanations.txt')
        self.sass_manager = ResourceManager('sass.txt')
        self.trump_manager = ResourceManager('trump.txt')

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        channel = self.clients.rtm.server.channels.find(channel_id)
        self.clients.send_user_typing_pause(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        help_txt = self.help_manager.get_all()
        count = self.help_manager.get_count()
        txt = (
            "I'm Flip Gunderson.  I'll respond to the following {} commands:\n{}"
        ).format(count-5, help_txt)
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_cast_pokemon(self, msg, channel_id):
        pkmn = self.pkmn_manager.cast_pkmn(msg)
        if pkmn is not None:
            self.send_message(channel_id, pkmn)
            
    def write_whos_that_pkmn(self, channel_id):
        txt = self.pkmn_manager.whos_that_pkmn(channel_id)
        self.send_message(channel_id, txt)
    
    def write_pkmn_guessed_response(self, msg_text, channel_id, user_id):
        txt = self.pkmn_manager.check_response(user_id, channel_id, msg_text)
        if txt is not None:
            self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def write_weather(self, channel_id):
        self.send_message(channel_id, weather_manager.getCurrentWeather())

    def write_flip(self, channel_id):
        self.send_message(channel_id, u"(╯°□°）╯︵ ┻━┻")

    def write_unflip(self, channel_id):
        self.send_message(channel_id, u"┬─┬ノ( º _ ºノ)")

    def write_blame(self, channel_id):
        self.send_message(channel_id, self.blame_manager.get_response())

    def write_explanation(self, channel_id):
        self.send_message(channel_id, self.explanation_manager.get_response())

    def write_sass(self, msg_txt, channel_id):
        target = self.__get_target(SASS_FLAG, msg_txt)
        if target == 'Kiera':
            sass = 'No. I like her.'
        else:
            if target == 'Flip Gunderson':
                prefix = 'Huh, nice try. '
                target = 'you'
            else:
                prefix = ''
            sass = '{}Hey, {}! {}'.format(prefix, target, self.sass_manager.get_response())
        self.send_message(channel_id, sass)

    def write_trump(self, channel_id):
        self.send_message(channel_id, self.trump_manager.get_response())


# PRIVATE METHODS:

    def __get_target(self, flag, msg_txt):
        token = re.split(flag, msg_txt.lower())
        target = ""
        if len(token) > 1:
            target = self.__format_target(token[1])
        return target

    def __format_target(self, target):
        if target == 'me':
            return 'you'
        elif target == 'yourself' or self.__is_flip_mention(target):
            return 'Flip Gunderson'
        elif self.__is_kiera_mention(target):
            return 'Kiera'
        elif '<@' in target:
            return target.upper()
        else:
            return target.title()

    def __is_flip_mention(self, msg_text):
        return re.search('flip', msg_text.lower())

    def __is_kiera_mention(self, msg_text):
        return re.search('kiera', msg_text.lower())
