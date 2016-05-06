# -*- coding: utf-8 -*-
import json
from urllib import urlopen, urlencode

class Plugin(object):

    def __init__(self, **kwargs): pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'define' and args:
            word =  self.search_urbandictionary(args)
            if word and 'definition' in word and 'word' in word:
                message = "{w}: {d}".format(w = word['word'].encode('utf-8'),
                                            d = word['definition'].replace("\n", "").replace("\r", "").encode('utf-8'))
                r = []
                if len(message) > 250:
                    if 'permalink' in word:
                        r.append((0, channel,
                                  "For more info: {u}".format(u = word['permalink'])))

                    r.append((0, channel, message[0:247] + "..."))
                else:
                    r.append((0, channel, message))

                if 'example' in word:
                    example = "Example: {e}".format(e = word['example'].replace("\n","").replace("\r","").encode('utf-8'))
                    if len(example) > 250:
                        r.append((0, channel, example[0:247] + "..."))
                    else:
                        r.append((0, channel, example))

                return r
            else:
                return [(0, channel,
                         "Sorry, I couldn't find \"{w}\"".format(w = args))]

    def search_urbandictionary(self, query):
        result = urlopen("http://api.urbandictionary.com/v0/define?" + urlencode({'term': query})).read()
        answer = json.loads(result)
        if 'result_type' in answer and answer['result_type'] == 'exact':
            return answer['list'][0]
        else:
            return False


if __name__ == '__main__':
    p = Plugin()
    print(p.cmd('define', 'GUI', 'test'))
    print(p.cmd('define', "Åhus", 'test'))
