# -*- coding: utf-8 -*-
from urllib import urlopen
from urllib import FancyURLopener
from random import randint, choice
from time   import time
import datetime
from kitchen.text.converters import to_bytes, to_unicode
import json
import re

class RedditOpener(FancyURLopener):
    version = 'Das hammermaessige bot/Python/urllib'
    #hdr = { 'User-Agent' : 'Das hammermaessige bot/Python/urllib' }

class Plugin:

    def __init__(self):
        self.aww_list = None
        self.aww_updated_at = None
        self.reddit_opener = RedditOpener()
        self.mornlist = [
            'Morn morn! ',
            'God morgen: ',
            'Morn! ',
            'Hvilken deilig morgen! ',
            'god morgen! ',
            'morgen! ',
            'god morgen ',
            'heia morgen! ',
            'ny dag. jippi! ',
            ]
        self.morn_re = re.compile(r'^(god|go)? ?mo(r|in)(gen|n)?', re.I)
        self.morndone = {}

    def cmd(self, command, args, channel, **kwargs):
        if command == 'aww' or command == 'sad' or command == 'depressed' or command == 'morn':
            if self.aww_updated_at == None or (time() - self.aww_updated_at) > 600:
                url = 'https://reddit.com/r/aww/hot.json?limit=100'
                self.aww_list = json.loads(self.reddit_opener.open(url).read())

                if 'error' in self.aww_list:
                    print(self.aww_list['error'])
                    return [(0, channel, kwargs['from_nick'],
                             'I\'m so sorry, Reddit gave me an error. :(')]
                else:
                    self.aww_updated_at = time()

            item = self.aww_list['data']['children'][randint(1,len(self.aww_list['data']['children']) - 1)]
            message = item['data']['url']
            nick = kwargs['from_nick']

            if args:
                args = args.split(' ')
                if len(args) >= 1 and len(args[0]) > 2:
                    nick = args[0]
                if len(args) == 2 and len(args[1]) > 2:
                    if args[1][0] == '#':
                        channel = args[1]
                    else:
                        channel = '#' + args[1]
            if command == 'morn':
                message = choice(self.mornlist) + message

            try:
                return[(0, channel, to_bytes(to_unicode(nick)), to_bytes(to_unicode(message)))]
            except:
                return[(0, channel, kwars['from_nick'], 'Couldn\'t convert to unicode. :(')]

    def listen(self, msg, channel, **kwargs):
        morn = self.morn_re.search(msg)
        if morn:
            today = datetime.datetime.now().date()
            if channel not in self.morndone or (channel in self.morndone and self.morndone[channel] != today):
                self.morndone[channel] = today
                return self.cmd('morn', None, channel, **kwargs)

if __name__ == '__main__':
    p = Plugin()
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
    print(p.cmd('aww', 'ÅssFøce', '#dasbot', from_nick='foo'))
    print(p.cmd('aww', 'AssFace foo', '#dasbot', from_nick='foo'))
    print(p.cmd('aww', 'AssFace #foo', '#dasbot', from_nick='foo'))
    print(p.listen('moin', '#dasbot', from_nick='foo'))
    print(p.listen('moin', '#dasbot', from_nick='foo'))
    print(p.listen('god morgen', '#dasbot', from_nick='foo'))
