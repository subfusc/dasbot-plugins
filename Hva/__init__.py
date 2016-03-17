# -*- coding: utf-8 -*-
#from GlobalConfig import *
import re
import duckduckgo # pip install duckduckgo2
from random import randint, choice


class Plugin(object):

    def __init__(self, **kwargs):
        self.hvaer = re.compile(r'(hva er|what is) (.*)', re.I) #[\?$]', re.I)
        #self.api = [line for line in open('apikey.txt', 'r')]
        self.last = {}

    def listen(self, msg, channel, **kwargs):
        hva = self.hvaer.search(msg)
        if hva:
            answer = self.ddg(hva.group(2))
            return [(0, channel, kwargs['from_nick'], answer)]

    def cmd(self, command, args, channel, **kwargs):
        if command[0] == '?':
            if len(command) > 1:
                if not args:
                    args = ""
                solve = command[1:] + args
            else:
                solve = args
            #print 'solve:' + solve
            answer = self.ddg(solve)
            if answer:
                return [(0, channel, kwargs['from_nick'], answer)]


    def ddg(self, query):
        r = duckduckgo.query(query)
        #print r.type
        if r.type == 'exclusive':
            return r.answer.text
        if r.type == 'disambiguation':
            return u'Is this what you think of: ' + r.related[0].text
        if r.type == 'answer':
            tmp = r.abstract.text
            tmp = self.smart_truncate(tmp) + ' (' + r.abstract.url + ')'
            return tmp
        else:
            return u'No idea'

    def smart_truncate(self, content, length=80, suffix='...'):
        print type(content)
        if len(content) <= length:
            return content
        else:
            return content[:length].rsplit(' ', 1)[0]+suffix



if __name__ == '__main__':
    print('done')
    p = Plugin()
    print(p.listen('Hva er 5*6?', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er 5 * 6', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er Oslo?', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er betasuppe?', '#iskbot', from_nick='foo'))
    print(p.listen('What is Oslo?', '#iskbot', from_nick='foo'))
    print(p.listen('hmmm. Hva er 5 * 6', '#iskbot', from_nick='foo'))
    print(p.cmd('?5 * 6', None, '#iskbot', from_nick='foo'))
    print(p.cmd('? oslo', None, '#iskbot', from_nick='foo'))
    print(p.cmd('? oslo + trondheim', None, '#iskbot', from_nick='foo'))
    print(p.cmd('?minecraft', None, '#iskbot', from_nick='foo'))
