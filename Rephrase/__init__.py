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
        self.lastsay = {}
        self.verylastsay = {}
        self.wlen = 4
        self.slen = 4
        pass

    def listen(self, msg, channel, **kwargs):
        if channel not in self.lastsay:
            self.lastsay[channel] = {}
        self.lastsay[channel][kwargs['from_nick']] = msg
        self.verylastsay[channel] = msg

    def stupid_tokenize(self, sent):
        sent = re.split('([ %s])' % (punctuation), sent, flags=re.UNICODE)
        return [w for w in sent if not w.startswith(' ')]

    def get_last_sent(self, nick, chan):
        # ikke i bruk
        log = 'data/log/%s.log' % (chan)
        try:
            log = open(log).readlines()
        except:
            print "Could not find file: ", log
        for line in reversed(log):
            line = line.split()
            log_nick = line[2].split("!")[0].split()[0].strip()
            if nick == log_nick :
                sent = ' '.join([w.lower() for w in line[4:]])
                if len(sent.split(" ") > self.slen):
                    return sent


    def pick_similar(self, word, lang):
        apisearch = "http://ltr.uio.no/semvec/%s/%s/api" % (lang, word)
        result = urlopen(apisearch).read()
        try:
            result = [l.split()[0] for l in result.split('\n')[2:]
                      if len(l) > 1]
            return random.choice(result)
        except:
            #  is unknown to the model
            return word

    def rephrase(self, sent, lang):
        sent = self.stupid_tokenize(sent)
        new_sent = []
        for word in sent:
            if len(word) > self.wlen:
                word = self.pick_similar(word, lang)
            new_sent.append(word)
        return ' '.join(new_sent)
    
    def pretty_print(self, sent):
        pp = "".join([w.strip() for w in re.split('([%s])' % (punctuation), sent)])
        pp = pp[0].upper() + pp[1:]
        return pp

    def cmd(self, command, args, channel, **kwargs):
        if command == 'rephrase':
            lang = 'norge'
            if args:
                args = args.split()
                if len(args) == 2:
                    lang = 'enwiki' # any 2. arg -> en
                args = args[0]
                if channel not in self.lastsay or args not in self.lastsay[channel]:
                    return [(0, channel, 'I have no memory of a last sentence from {}'.format(args))]
            elif channel not in self.verylastsay:
                return [(0, channel, 'I have no memory of a last sentence'.format(args))]
            rephrased = self.rephrase(self.lastsay[channel][args], lang)
            rephrased = self.pretty_print(rephrased)
            return [(0, channel, rephrased)]

if __name__ == '__main__':
    print('done')
    p = Plugin()
    p.listen('Slip them into different sleeves! Buy both, and be deceived', '#bar', from_nick = 'baz')
    print p.cmd('rephrase', 'baz en', '#bar')
    p.listen('Ingenting er morsommere enn hammermessige irc-botter.', '#bar', from_nick = 'baz')
    print p.lastsay
    print p.cmd('rephrase', 'baz', '#bar')
