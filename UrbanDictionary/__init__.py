import json
from urllib import urlopen
from cgi import escape

class Plugin(object):

    def __init__(self, **kwargs): pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'define' and args:
            search_query = escape(args)
            word =  self.search_urbandictionary(search_query)
            if word and 'definition' in word and 'word' in word:
                message = "{w}: {d}".format(w = word['word'].encode('utf-8'),
                                            d = word['definition'].replace("\n", "").replace("\r", "").encode('utf-8'))
                if len(message) > 250:
                    r = []
                    if 'permalink' in word:
                        r.append((0, channel,
                                  "For more info: {u}".format(u = word['permalink'])))
                    if 'example' in word:
                        r.append((0, channel,
                                  "Example: {e}".format(e = word['example'].encode('utf-8'))[0:247] + "..."))
                    r.append((0, channel, message[0:247] + "..."))
                    return r
                else:
                    return [(0, channel, message)]
            else:
                return [(0, channel,
                         "Sorry, I couldn't find \"{w}\"".format(w = args))]

    def search_urbandictionary(self, query):
        result = urlopen("http://api.urbandictionary.com/v0/define?term=" + query).read()
        answer = json.loads(result)
        if 'result_type' in answer and answer['result_type'] == 'exact':
            return answer['list'][0]
        else:
            return False
