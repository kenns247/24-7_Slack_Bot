import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            msg_txt = event['text']
            lower_txt = msg_txt.lower()
            channel_id = event['channel']
            user_id = event['user']

            # Triggers that require @flip mentions
            if self.clients.is_bot_mention(msg_txt):
                if re.search('help', lower_txt):
                    self.msg_writer.write_help_message(event['channel'])
                    return
                if re.search('weather', lower_txt):
                    self.msg_writer.write_weather(channel_id)
                    return
                if re.search('hi |hey|hello|howdy', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                    return
                if re.search('unflip', lower_txt):
                    self.msg_writer.write_unflip(channel_id)
                    return
                elif re.search('rage|flip|rageflip|tableflip', lower_txt):
                    self.msg_writer.write_flip(channel_id)
                    return
                if re.search('joke', lower_txt):
                    self.msg_writer.write_joke(event['channel'])
                    return
                if re.search('attachment', lower_txt):
                    self.msg_writer.demo_attachment(event['channel'])
                    return       
                if re.search('echo', lower_txt):
                    self.msg_writer.send_message(event['channel'], msg_txt)
                    return
                if re.search('i choose you', lower_txt):
                    self.msg_writer.write_cast_pokemon(lower_txt, channel_id)
                    return
                if re.search('who\'?s that pokemon', lower_txt):
                    self.msg_writer.write_whos_that_pkmn(channel_id)
                    return
                if re.search('it\'?s ', lower_txt):
                    self.msg_writer.write_pkmn_guessed_response(lower_txt, channel_id, user_id)
                    return
                if re.search('sass ', lower_txt):
                    self.msg_writer.write_sass(msg_txt, channel_id)
                    return
                elif re.search('who', lower_txt):
                    self.msg_writer.write_blame(channel_id)
                    return
                elif re.search('why ', lower_txt):
                    self.msg_writer.write_explanation(channel_id)
                    return

            # Triggers that don't require @flip mentions
            if re.search('trump', lower_txt):
                self.msg_writer.write_trump(channel_id)
                return
            
            # Else ignore it
            else:
                pass
