from random import randint
from urllib import urlopen
from xml.sax.saxutils import unescape

class Plugin(object):

    def __init__(self, **kwargs):
        self.shake_insults = self.read_shake()

    def read_shake(self):
        shake_lists = [[], [], []]
        for line in open("data/shakespeare_insult.txt"):
            a, b, c = line.split()
            shake_lists[0].append(a)
            shake_lists[1].append(b)
            shake_lists[2].append(c)
        return shake_lists

    def cmd(self, command, args, channel, **kwargs):
        if command == 'insult' and args:
            insultee = args
            return [(0, channel, self.get_insult(insultee))]

    def get_insult(self, insultee):
        try:
            if randint(1, 2) == 1:
                result = self.from_insult_generator(insultee)
            else:
                result = self.from_shake(insultee)
        except:
            result = "I could not find an appropriate way to insult %s. Which says it all, really." % (insultee)
        return result


    def from_insult_generator(self, insultee):
        result = urlopen("http://www.insultgenerator.org/").read()
        result = result.split("<br><br>")[1].split("</div>")[0].strip()
        result = unescape(result)
        if "&nbsp;" in result:
            result = " ".join(result.split("&nbsp;"))
        return "{w}: {insult}".format(w = insultee, insult = result)

    def from_shake(self, insultee):
        length = len(self.shake_insults[0]) - 1
        return "%s, you %s %s %s" % (insultee,
                                     self.shake_insults[0][randint(0, length)],
                                     self.shake_insults[1][randint(0, length)],
                                     self.shake_insults[2][randint(0, length)])
