# -*- coding: utf-8 -*-
from urllib import urlopen
from urllib import FancyURLopener
from random import randint
from time   import time
import json

class RedditOpener(FancyURLopener):
    version = 'Das hammermaessige bot/Python/urllib' 
    #hdr = { 'User-Agent' : 'Das hammermaessige bot/Python/urllib' }

class Plugin:

    def __init__(self):
        self.aww_list = None
        self.aww_updated_at = None
        self.reddit_opener = RedditOpener()

    def cmd(self, command, args, channel, **kwargs):
        if command == 'aww' or command == 'sad' or command == 'depressed':
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
            return [(0, channel, kwargs['from_nick'], item['data']['url'])]

if __name__ == '__main__':
    p = Plugin()
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
    print(p.cmd('aww', None, '#dasbot', from_nick='foo'))
