# -*- coding: utf-8 -*-
from urllib import urlopen
from random import randint
import json

class Plugin:

    def __init__(self): pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'aww' or command == 'sad' or command == 'depressed':
            url = 'https://reddit.com/r/aww/hot.json?limit=100'
            aww = json.loads(urlopen(url).read())

            if 'error' in aww:
                print(aww['error'])
                return [(0, channel, kwargs['from_nick'],
                         'I\'m so sorry, Reddit gave me an error. :(')]

            item = aww['data']['children'][randint(1,len(aww['data']['children']) - 1)]
            return [(0, channel, kwargs['from_nick'], item['data']['url'])]

if __name__ == '__main__':
    p = Plugin()
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
