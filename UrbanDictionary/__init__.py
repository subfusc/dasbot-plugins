import json
from urllib import urlopen
from cgi import escape

class Plugin(object):

    def __init__(self, **kwargs): pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'define':
            search_query = escape(args)
            result =  self.search_urbandictionary(search_query)
            if result:
                return [(0, channel, result)]
            else:
                return [(0, channel, "Sorry, I couldn't find {w}".format(w = args))]

    def search_urbandictionary(self, query):
        result = urlopen("http://api.urbandictionary.com/v0/define?term=" + query).read()
        answer = json.loads(result)
        if 'result_type' in answer and answer['result_type'] == 'exact':
            word = answer['list'][0]
            return "{w}: {d}".format(w = word['word'],
                                     d = word['definition'])
