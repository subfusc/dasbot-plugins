import json
from urllib import urlopen
from xml.sax.saxutils import unescape

class Plugin(object):

    def __init__(self, **kwargs): pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'insult' and args:
            insultee = args
            return [(0, channel,
                         "{w}: {insult}".format(w = insultee, 
                                                insult = self.get_insult()))]
            
    def get_insult(self):
        try:
            result = urlopen("http://www.insultgenerator.org/").read()
            result = result.split("<br><br>")[1].split("</div>")[0].strip()
            result = unescape(result)
            if "&nbsp;" in result:
                result = " ".join(result.split("&nbsp;"))
        except:
            result = "I could not find an appropriate insult for you. Which says it all, really."
        return result