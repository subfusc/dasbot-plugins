# -*- coding: utf-8 -*-
#from GlobalConfig import *
import re
import duckduckgo # pip install duckduckgo2
import urllib3
urllib3.disable_warnings()
import wikipedia
from random import randint, choice
import string
import time
try:
    import GlobalConfig as conf
except:
    pass

class Plugin(object):

    def __init__(self, **kwargs):
        self.stopwords_no = set(["alle", "andre", "arbeid", "av", "begge", "bort", "bra", "bruke", "da", "denne", "den", "der", "deres", "det", "din", "disse", "du", "eller", "en", "ene", "eneste", "enhver", "enn", "er", "et", "folk", "for", "fordi", "forsøke", "fra", "få", "før", "først", "gjorde", "gjøre", "god", "gå", "ha", "hadde", "han", "hans", "hennes", "her", "hva", "hvem", "hver", "hvilken", "hvis", "hvor", "hvordan", "hvorfor", "i", "ikke", "inn", "innen", "kan", "kunne", "lage", "lang", "lik", "like", "makt", "mange", "med", "meg", "meget", "men", "mens", "mer", "mest", "min", "mye", "må", "måte", "navn", "nei", "ny", "nå", "når", "og", "også", "om", "opp", "oss", "over", "part", "problemet", "punkt", "på", "rett", "riktig", "samme", "sant", "si", "siden", "sist", "skulle", "slik", "slutt", "som", "start", "stille", "så", "tid", "til", "tilbake", "tilstand", "under", "ut", "uten", "var", "ved", "verdi", "vi", "vil", "ville", "vite", "vår", "være", "vært", "å"])
        self.stopwords_en = set(["a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did", "differ", "different", "differently", "do", "does", "done", "down", "down", "downed", "downing", "downs", "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "high", "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest", "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making", "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much", "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer", "newest", "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off", "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens", "or", "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted", "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible", "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r", "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show", "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some", "somebody", "someone", "something", "somewhere", "state", "states", "still", "still", "such", "sure", "t", "take", "taken", "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing", "things", "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to", "today", "together", "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until", "up", "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way", "ways", "we", "well", "wells", "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole", "whose", "why", "will", "with", "within", "without", "work", "worked", "working", "works", "would", "x", "y", "year", "years", "yet", "you", "young", "younger", "youngest", "your", "yours", "z"])

        self.hvaer = re.compile(r'hva er ([^\?]*)\??', re.I) #[\?$]', re.I)
        self.whatis = re.compile(r'what is ([^\?]*)\??', re.I) #[\?$]', re.I)
        self.wp_no_ignoreline = re.compile(r'kan ha andre betydninger', re.I)
        self.wp_en_ignoreline = re.compile(r'For other uses', re.I)
        self.q_art = re.compile(r'^(a|an|en|et)$', re.I)
        #self.api = [line for line in open('apikey.txt', 'r')]
        self.last = {}

    def help(self, command, argc, channel, **kwargs):
        if command == 'all':
            return [(1, kwargs['from_nick'], 'Hva: ?, hva, what')]
        if command == 'hva' or command == '?' or command == 'what':
            return [(1, kwargs['from_nick'], conf.COMMAND_CHAR + command + " [-lang] [query]"),
             (1, kwargs['from_nick'], "Gives answer. Are also trigged by hva er [query]? and what are [query]?")]

    def remove_art(self, query):
        q = query.split()
        if len(q) > 1:
            if self.q_art.match(q[0]):
                return "".join(q[1:])
        return query

    def listen(self, msg, channel, **kwargs):
        hva = self.hvaer.search(msg)
        msg_split = msg.split()
        if len(msg_split) > 2:
            forste_ord = msg.split()[2].translate(string.maketrans("",""), string.punctuation)
            #print forste_ord
            if hva and forste_ord.lower() not in self.stopwords_no:
                query = self.remove_art(hva.group(1))
                answer = self.ddg(query, lang='no')
                if answer:
                    return [(0, channel, kwargs['from_nick'], answer)]
            what = self.whatis.search(msg)
            if what and forste_ord.lower() not in self.stopwords_en:
                query = self.remove_art(what.group(1))
                answer = self.ddg(query, lang='en')
                if answer:
                    return [(0, channel, kwargs['from_nick'], answer)]

    def cmd(self, command, args, channel, **kwargs):
        if (len(command) > 1 and command[0] == '?') or command == 'hva' or command == 'what':
            lang = 'en'
            if command[0] == '?' and len(command) > 1:
                if not args:
                    args = ""
                query = command[1:] + args
            elif args and len(args) > 0:
                argssplit = args.split(None, 1)
                if argssplit[0][0] == '-':
                    if len(argssplit) < 2:
                        return [(1, kwargs['from_nick'], "Usage: " + conf.COMMAND_CHAR + command + " [-lang] [query]")]
                    query = argssplit[1]
                    lang = argssplit[0][1:]
                    answer = self.wp(query.strip(), lang=lang).encode('utf-8')
                    if answer:
                        return [(0, channel, kwargs['from_nick'], answer)]
                    else:
                        return [(0, channel, kwargs['from_nick'], "Sorry, I have no idea.")]
                else:
                    query = args
            else:
                return [(0, channel, kwargs['from_nick'], "Look. Up in the sky. It's a bird. It's a plane. No. It's just the void. Infinite and indifferent. We're so small. So very very small.")]
            answer = self.ddg(query.strip(), lang=lang)
            if answer:
                return [(0, channel, kwargs['from_nick'], answer)]
            else:
                return [(0, channel, kwargs['from_nick'], "Sorry, I have no idea.")]

    def ddg_chose(self, related):
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
        if self.wp_en_ignoreline.search(summary) or self.wp_no_ignoreline.search(summary):
            summary = ""
        summary = summary.replace('?/i', "")
        summary, num = self.remove_brackets(summary, 0)
        summary = summary.replace('  ', ' ')
        return summary

    def wp(self, query, lang='en'):
        wikipedia.set_lang(lang)
        try:
            s = wikipedia.summary(query)
            summarylist = s.splitlines()
        except:
            print "exception"
            summarylist = []
        summary = ""
        while len(summarylist) > 0 and len(summary.split()) < 4:
            summary = summarylist.pop(0)
            summary = self.wp_clean(summary)
        return self.smart_truncate(summary)

    def wp_run(self, query, lang='en'):
        wik = self.wp(query, lang=lang)
        if wik:
            if lang == 'no':
                tmp = wik # self.ddg_chose(r.related)
            else:
                tmp = wik # self.ddg_chose(r.related)
            tmp = tmp.encode('utf-8')
            return tmp
        return ""

    def ddg(self, query, lang='en'):
        r = duckduckgo.query(query)
        if r.type == 'exclusive':
            return r.answer.text.encode('utf-8')
        if r.type == 'disambiguation':
            wik = self.wp_run(query, lang)
            if wik:
                return wik
            elif len(r.related) > 0:
                tmp = u'Is this what you think of: ' + self.ddg_chose(r.related)
                tmp = tmp.encode('utf-8')
                return tmp
            else:
                return u'My head hurts :(.'
        if r.type == 'answer':
            tmp = r.abstract.text
            tmp = self.smart_truncate(tmp) + ' (' + r.abstract.url + ')'
            tmp = tmp.encode('utf-8')
            return tmp
        else:
            wik = self.wp_run(query, lang)
            if wik:
                return wik
            return None
            #return u'No idea'

    def smart_truncate(self, content, length=100, suffix='...'):
        if len(content) <= length:
            return content
        else:
            return content[:length].rsplit(' ', 1)[0]+suffix



if __name__ == '__main__':
    p = Plugin()
    #print(p.listen('Hva er 5*6?', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er 5 * 6', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er Oslo?', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er bil?', '#iskbot', from_nick='foo'))
    print(p.listen('What is car', '#iskbot', from_nick='foo'))
    print(p.listen('Hva er det?', '#iskbot', from_nick='foo'))
    print(p.listen('What is that', '#iskbot', from_nick='foo'))
    #print(p.listen('Hva er betasuppe?', '#iskbot', from_nick='foo'))
    #print(p.listen('What is Oslo?', '#iskbot', from_nick='foo'))
    #print(p.listen('hmmm. Hva er 5 * 6', '#iskbot', from_nick='foo'))
    #print(p.listen('What is 5?', '#iskbot', from_nick='foo'))
    #print(p.cmd('?5 * 6', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?oslo', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?', 'oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-de oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-no oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-en oslo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-en Apple', '#iskbot', from_nick='foo'))
    #print(p.cmd('?minecraft', None, '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-sv minecraft', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-ja totoro', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', '-ja Volvo', '#iskbot', from_nick='foo'))
    #print(p.cmd('?', None, '#iskbot', from_nick='foo'))
