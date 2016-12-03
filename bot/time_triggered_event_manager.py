from datetime import datetime, timedelta
from channel_manager import ChannelManager
from resource_manager import ResourceManager
import time
import random

HR_DIF_DST = 5  # for Winnipeg
HR_DIF_NO_DST = 6  # for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

global HAS_TRIGGERED_THIS_HOUR

class TimeTriggeredEventManager(object):
    def __init__(self, clients, msg_writer):
        HAS_TRIGGERED_THIS_HOUR = False
        self.clients = clients
        self.msg_writer = msg_writer
        self.channel_manager = ChannelManager(clients)
        self.tea_manager = ResourceManager('tea.txt')
        self.wake_me_up_mananger = ResourceManager('wake_me_up.txt')

    def trigger_eleven_eleven(self):
        channel_id = self.channel_manager.get_channel_id('general')
        response = '<!channel> 11:11 is in 11 minutes!! Grab some :coffee: and then hit the bleachers!'
        self.msg_writer.send_message(channel_id, response)

    def trigger_standup(self):
        channel_id = self.channel_manager.get_channel_id('general')
        response = '<!channel> Time for stand-up!!'
        emojis = [':dancers:', ':dancer:', ':raised_hands:', ':up:']
        response = '{} {}'.format(response, random.choice(emojis))
        self.msg_writer.send_message(channel_id, response)
    
    def trigger_teatime(self):
        channel_id = self.channel_manager.get_channel_id('general')
        channel = '<!channel>'
        phrase = self.tea_manager.get_response()
        tea_emoji = ':tea:'
        response = '{} {} {}'.format(channel, phrase, tea_emoji)
        self.msg_writer.send_message(channel_id, response)

    def trigger_wake_me_up(self):
        if random.random() < 0.01:
            HAS_TRIGGERED_THIS_HOUR = True
            channel_id = self.channel_manager.get_channel_id('flip_testing')
            response = self.wake_me_up_mananger.get_response()
            self.msg_writer.send_message(channel_id, response)

    def trigger_timed_event(self):
        day, hour, minute, second = self._get_datetime()
        
        # leaves 10-ish seconds to trigger since method is called every 10-ish
        # seconds and we wantz the if statement to trigger once per min only
        if(second >= 5 and second <= 15):
            # reset triggered value to false every hour
            if minute == 0:
                HAS_TRIGGERED_THIS_HOUR = False
            # Wake Up Randoms
            if hour >= 9 and hour <= 17 and HAS_TRIGGERED_THIS_HOUR == False:
                self.trigger_wake_me_up()
            if (day != 'Saturday' and day != 'Sunday'):
                # Stand Up
                if hour == 10 and minute == 30:
                    self.trigger_standup()
                # Tea Time
                if hour == 15 and minute == 0:
                    self.trigger_teatime()                
            if day == 'Monday':
                # 11:11
                if hour == 11 and minute == 0:
                    self.trigger_eleven_eleven()

    def _get_datetime(self):
        curr_datetime = datetime.utcnow() - timedelta(hours=HR_DIF_NO_DST)
        day = curr_datetime.strftime('%A')
        hour = int(curr_datetime.strftime('%H'))
        minute = int(curr_datetime.strftime('%M'))
        second = int(curr_datetime.strftime('%S'))
        return day, hour, minute, second