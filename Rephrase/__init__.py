import sys
import string
import random
import codecs
from string import punctuation
from kitchen.text.converters import to_bytes, to_unicode
import os
import re
from itertools import chain
from urllib import urlopen

class Plugin(object):
    def __init__(self, **kwargs):
        pass

    def stupid_tokenize(self, sent):
        sent = re.split('([ %s])' % (punctuation), sent, flags=re.UNICODE)
        return [w for w in sent if not w.startswith(' ')]

    def get_last_sent(self, nick, chan):
        log = 'data/log/%s.log' % (chan)
        try:
            log = open(log).readlines()
        except:
            print "SHIT: ", log
        for line in reversed(log):
            line = line.split()
            log_nick = line[2].split("!")[0].split()[0].strip()
            if nick == log_nick :
                sent = ' '.join([w.lower() for w in line[4:]])
                if len(sent.split(" ") > 4:
                    return sent


    def pick_similar(self, word):
        apisearch = "http://ltr.uio.no/semvec/%s/%s/api" % ('norge', word)
        result = urlopen(apisearch).read()
        try:
            if result:
                result = [l.split()[0] for l in result.split('\n')[2:]
                          if len(l) > 1]
                return random.choice(result)
        except:
            return word

    def rephrase(self, sent):
        sent = self.stupid_tokenize(sent)
        new_sent = []
        for word in sent:
            if len(word) > 5:
                word = self.pick_similar(word)
            new_sent.append(word)
        return ' '.join(new_sent)

    def cmd(self, command, args, channel, **kwargs):
        if command == 'rephrase' and args:
            last_sent = self.get_last_sent(args.strip(), channel.strip("#"))
            rephrased = self.rephrase(last_sent)
            return [(0, channel, rephrased)]

if __name__ == '__main__':
    print('done')
    p = Plugin()
    p.cmd('rephrase', 'tanyabt', '#termvakt-fjas')
