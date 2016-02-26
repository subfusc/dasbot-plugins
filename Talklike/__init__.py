import sys
import string
import random
import codecs
from string import punctuation
from kitchen.text.converters import to_bytes, to_unicode
import os

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
        return words


    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

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

    def generate_markov_text(self, size=10):

        w1, w2 = ('#', '#')
        while True:
            seed = random.randint(0, self.word_size-3)
            w1, w2 = self.words[seed], self.words[seed+1]
            if (w1, w2) in self.cache:
                break
        gen_words = []
        for i in xrange(size):
            if (w1, w2) in self.cache:
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
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


    def get_nick_data(self, log):
        nick_data = {}
        for line in log:
            # print line
            line = line.split()
            if len(line) > 10:
                nick = line[2].split("!")[0].split()[0].strip()
                text = ' '.join([ w.lower() for w in line[4:] if w[0] not in punctuation])
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
                blurb = self.hmms[channel[1:]][args.strip()].generate_markov_text(30)
                blurb = blurb.split('.')[0] + '.'
                try:
                    print blurb.decode('utf8')
                except:
                    print "unicode error"
            else:
                blurb = "I don't know this '%s'." % (args)
            try:
                return [(0, channel, to_bytes(to_unicode(blurb)))]
            except:
                return [(0, channel, kwars['from_nick'], 'Couldn\'t convert to unicode. :(')]

if __name__ == '__main__':
    print('done')
    p = Plugin()
    p.cmd('talklike', 'trondth', 'termvakt-fjas')

