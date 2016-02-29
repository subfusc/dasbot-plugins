import sys
import string
import random
import codecs
from string import punctuation
from kitchen.text.converters import to_bytes, to_unicode
import os
import re
from itertools import chain

NONOCHARS = "\"'()[]\{\}"

class Markov(object):
    def __init__(self, data):
        self.cache = {}
        self.words = self.to_words(data)
        self.word_size = len(self.words)
        self.database()


    def to_words(self, data):
        #random.shuffle(data)
        data = string.join(data, '')
        words = data.split()
        actual_words = []
        for w in words:
            if w[0] in NONOCHARS:
                w = w[1:]
            if w[-1] in NONOCHARS:
                w = w[:-1]
            actual_words.append(w)
        #words = re.split("[\W+]", data)
        return actual_words


    def triples(self):
        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size):
        w1, w2 = ('#', '#')
        while True:
            seed = random.randint(0, self.word_size - 2)
            w1, w2 = self.words[seed], self.words[seed+1]
            if (w1, w2) in self.cache:
                break
        gen_words = []
        for i in xrange(size):
            if (w1, w2) in self.cache:
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        while gen_words:
            if len(gen_words[-1]) > 4:
                break
            else:
                gen_words = gen_words[:-1]
        return ' '.join(gen_words)

class Plugin(object):
    def __init__(self, **kwargs):
        self.hmms = {}
        for crap, shit, logger in os.walk("data/log/"):
            for file in logger:
                if file.endswith(".log"):
                    chan = file[:-4]
                    print 'chan: ', chan
                    log = open('data/log/%s' % (file)).readlines()
                    if chan not in self.hmms:
                        self.hmms[chan] = {}
                    nick_data = self.get_nick_data(log)
                    for nick in nick_data:
                        self.hmms[chan][nick] = Markov(nick_data[nick])


    def get_random_end(self):
        # crazy strategy for skewing probabilities!!!11
        period =      ['.'     for x in range(20)]
        bang =        ['!'     for x in range(10)]
        question =    ['?'     for x in range(5)]
        triple_bang = ['!!!'   for x in range(2)]
        smile =       [':-)'   for x in range(1)]
        ironic =      ['!!!11' for x in range(1)]
        suspense =    ['...'   for x in range(2)]
        joined = [x for x in chain(period, bang, question, triple_bang, smile, ironic, suspense)]
        return random.choice(joined)

    def get_nick_data(self, log):
        nick_data = {}
        for line in log:
            # print line
            line = line.split()
            if len(line) > 10:
                nick = line[2].split("!")[0].split()[0].strip()
                text = ' '.join([w.lower() for w in line[4:] if w[0] not in punctuation])
                if not nick in nick_data:
                    nick_data[nick] = []
                nick_data[nick].append(text + '\n')
        return nick_data

    def cmd(self, command, args, channel, **kwargs):
        if command == 'talklike' and args:
            print 'talklike: ' + channel
            print self.hmms.keys()
        #if channel in self.hmms:
            if channel[1:] in self.hmms and args.strip() in self.hmms[channel[1:]]:
                blurb = self.hmms[channel[1:]][args.strip()].generate_markov_text(25)
                if blurb[-1] not in punctuation:
                    blurb = blurb + self.get_random_end()
                try:
                    print blurb.decode('utf8')
                except:
                    print "unicode error"
            else:
                blurb = "I don't know this '%s'." % (args)
            try:
                return [(0, channel, to_bytes(to_unicode(blurb)))]
            except:
                return [(0, channel, kwargs['from_nick'], 'Couldn\'t convert to unicode. :(')]

if __name__ == '__main__':
    print('done')
    p = Plugin()
    p.cmd('talklike', 'tanyabt', '#termvakt-fjas')
