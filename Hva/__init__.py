# -*- coding: utf-8 -*-
#from GlobalConfig import *
import regex as re
import duckduckgo # pip install duckduckgo2
import urllib3
urllib3.disable_warnings()
import wikipedia
from random import randint, choice
import time

class Plugin(object):

    def __init__(self, **kwargs):
        self.hvaer = re.compile(r'hva er ([^\?]*)\??', re.I) #[\?$]', re.I)
        self.whatis = re.compile(r'what is ([^\?]*)\??', re.I) #[\?$]', re.I)
        #TODO hoppe over linjer med slikt innhold:
        self.wp_no_ignoreline = re.compile(r'kan ha andre betydninger', re.I)
        self.wp_en_ignoreline = re.compile(r'For other uses', re.I)
        #self.api = [line for line in open('apikey.txt', 'r')]
        self.last = {}

    def listen(self, msg, channel, **kwargs):
        hva = self.hvaer.search(msg)
        if hva:
            answer = self.ddg(hva.group(1), lang='no')
            return [(0, channel, kwargs['from_nick'], answer)]
        what = self.whatis.search(msg)
        if what:
            answer = self.ddg(what.group(1), lang='en')
            return [(0, channel, kwargs['from_nick'], answer)]

    def cmd(self, command, args, channel, **kwargs):
        if command[0] == '?' or command == 'hva' or command == 'what':
            lang = 'en'
            if command[0] == '?' and len(command) > 1:
                if not args:
                    args = ""
                query = command[1:] + args
            elif len(args) > 0:
                argssplit = args.split(None, 1)
                if len(argssplit[0]) == 3 and argssplit[0][0] == '-':
                    query = argssplit[1]
                    lang = argssplit[0][1:]
                    print "lang: {}".format(lang)
                    answer = self.wp(query.strip(), lang=lang).encode('utf-8')
                    if answer:
                        return [(0, channel, kwargs['from_nick'], answer)]
                else:
                    query = args
            else:
                query = 'void'
            print 'query:' + query
            answer = self.ddg(query.strip(), lang=lang)
            if answer:
                return [(0, channel, kwargs['from_nick'], answer)]

    def ddg_chose(self, related):
        #print "type: {}".format(type(related))
        for it in related:
            if it.topics: # and it.topics.name != 'See also':
                return self.ddg_chose(it.topics)
            elif it.text:
                return it.text
            else:
                pass
        return False

    def remove_brackets(self, s, i, inside=False):
        string = ""
        while i < len(s):
            if s[i] == '(':
                tmp, i = self.remove_brackets(s, i+1, inside=True)
            elif s[i] == ')':
                return None, i+1
            else:
                if not inside:
                    string += s[i]
                i += 1
        return string, i

    def wp_clean(self, summary):
        summary = summary.replace('?/i', "")
        summary, num = self.remove_brackets(summary, 0)
        summary = summary.replace('  ', ' ')
        return summary

    def wp(self, query, lang='en'):
        #print '...{}...'.format(query)
        wikipedia.set_lang(lang)
        #print "|{}|".format(lang)
        #print "|{}|".format(query)
        #time.sleep(1)
        summarylist = wikipedia.summary(query).splitlines()
        summary = ""
        while len(summarylist) > 1 and len(summary.split()) < 4:
            summary = summarylist.pop(0)
            summary = self.wp_clean(summary)
        return self.smart_truncate(summary)

    def ddg(self, query, lang='en'):
        print "1{}1".format(query)
        r = duckduckgo.query(query)
        #print r.type
        if r.type == 'exclusive':
            return r.answer.text.encode('utf-8')
        if r.type == 'disambiguation':
            wik = self.wp(query, lang=lang)
            if wik:
                if lang == 'no':
                    tmp = wik # self.ddg_chose(r.related)
                else:
                    tmp = wik # self.ddg_chose(r.related)
                tmp = tmp.encode('utf-8')
                return tmp
            elif len(r.related) > 0:
                tmp = u'Is this what you think of: ' + self.ddg_chose(r.related)
                tmp = tmp.encode('utf-8')
                return tmp
            else:
                return u'My head hurts :(.'
                #print type(tmp)
        if r.type == 'answer':
            tmp = r.abstract.text
            tmp = self.smart_truncate(tmp) + ' (' + r.abstract.url + ')'
            tmp = tmp.encode('utf-8')
            return tmp
        else:
            return u'No idea'

    def smart_truncate(self, content, length=100, suffix='...'):
        #print type(content)
        if len(content) <= length:
            return content
        else:
            return content[:length].rsplit(' ', 1)[0]+suffix



if __name__ == '__main__':
    print('done')
    p = Plugin()
    #print(p.listen('Hva er 5*6?', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er 5 * 6', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er Oslo?', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er betasuppe?', '#iskbot', from_nick='foo'))
    #print(p.listen('What is Oslo?', '#iskbot', from_nick='foo'))
    #print(p.listen('hmmm. Hva er 5 * 6', '#iskbot', from_nick='foo'))
    #print(p.listen('What is 5?', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er trond', '#iskbot', from_nick='foo'))
    #print(p.listen('What is trond', '#iskbot', from_nick='foo'))
    #print(p.cmd('?5 * 6', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?oslo', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?', 'oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-de oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-no oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-en oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-en Apple', '#iskbot', from_nick='foo'))
    #print(p.cmd('?minecraft', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-sv minecraft', '#iskbot', from_nick='foo'))

