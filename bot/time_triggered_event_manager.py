from datetime import datetime, timedelta
from channel_manager import ChannelManager
import time

HR_DIF_DST = 5  # for Winnipeg
HR_DIF_NO_DST = 6  # for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

class TimeTriggeredEventManager(object):
    def __init__(self, clients, msg_writer):
        self.clients = clients
        self.msg_writer = msg_writer
        self.channel_manager = ChannelManager(clients)

    def trigger_eleven_eleven(self):
        channel_id = self.channel_manager.get_channel_id('flip-testing')
        response = '<!channel> 11:11 is in 11 minutes!! Grab some :coffee: and then hit the bleachers!'
        self.msg_writer.send_message(channel_id, response)

    def trigger_timed_event(self):
        day, hour, minute, second = _get_datetime()

        # leaves 10-ish seconds to trigger since method is called every 10-ish
        # seconds and we wantz the if statement to trigger once per min only
        if(second >= 5 and second <= 15):
            if day == 'Sunday':
                if hour == 16 and minute == 43:
                    self.trigger_eleven_eleven()

    def _get_datetime():
        curr_datetime = datetime.utcnow() - timedelta(hours=HR_DIF_NO_DST)
        day = curr_datetime.strftime('%A')
        hour = int(curr_datetime.strftime('%H'))
        minute = int(curr_datetime.strftime('%M'))
        second = int(curr_datetime.strftime('%S'))
        return day, hour, minute, second