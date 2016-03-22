# -*- coding: utf-8 -*-
import re
from time import strftime

class Plugin(object):

    def __init__(self, **kwargs):
        self.logg_file = 'data/log/{}.log'
        self.last_seen = {}
        self.monitored_channels = {}
        self.log_re = re.compile(r'^\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\]\s(?P<nick>[^!]+?)![^@]+?@\S+?\s((<.\d{2}(\w+)\W?>.+)|(.\d{2}(\w+). (left|joined) the game.))$')
        self.monitor_re = re.compile(r'^(<.\d{2}(\w+)\W?>.+)|(.\d{2}(\w+)\W? (left|joined) the game.)$')

    def _connect_channel(self, channel, nick):
        self.monitored_channels[channel] = nick
        log = open(self.logg_file.format(channel)).readlines()
        self.last_seen[channel] = {}
        for line in log:
            match = self.log_re.search(line)
            if match and nick == match.group('nick'):
                self.last_seen[channel][match.group(5) or match.group(7)] = match.group(1)

    def _has_seen(self, channel, user):
        if channel in self.last_seen and user in self.last_seen[channel]:
            return self.last_seen[channel][user]
        else:
            return 'Unseen'

    def cmd(self, cmd, args, channel, **kwargs):
        if cmd == 'identify-mc-spammer' and kwargs['auth_level'] > 50:
            self._connect_channel(channel.strip('#'), args)
            return [(0, channel, 'I see you {}!'.format(args))]
        elif cmd == 'mc-last-seen' and args:
            return [(0, channel, kwargs['from_nick'], self._has_seen(channel.strip('#'), args))]

    def listen(self, msg, channel, **kwargs):
        channel = channel.strip('#')
        if channel in self.monitored_channels and self.monitored_channels[channel] == kwargs['from_nick']:
            match = self.monitor_re.match(msg)
            if match:
                self.last_seen[channel][match.group(2) or match.group(4)] = strftime('%F %T')

if __name__ == '__main__':
    p = Plugin()
    print p.cmd('identify-mc-spammer', 'gloop-mc', '#gloop', auth_level=51)
    print p.cmd('mc-last-seen', 'lebchen', '#gloop', from_nick='foo')
    p.listen('<b23lebchenxxx.> hvis man har en og det ikke står noe tall altså :P', '#gloop', from_nick='gloop-mc')
    p.listen('<b23lebchenxyx.> left the game.', '#gloop', from_nick='gloop-mc')
    p.listen('<b23lebchenxyz.> joined the game.', '#gloop', from_nick='gloop-mc')
    print p.last_seen
