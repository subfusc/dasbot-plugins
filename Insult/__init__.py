from random import randint
from urllib import urlopen
from xml.sax.saxutils import unescape

class Plugin(object):

    def __init__(self, **kwargs):
        self.shake_insults = self.read_shake()

    def read_shake(self):
        shake_lists = [[], [], []]
        for line in self.shakestring().split('\n'):
            a, b, c = line.split()
            shake_lists[0].append(a)
            shake_lists[1].append(b)
            shake_lists[2].append(c)
        return shake_lists

    def cmd(self, command, args, channel, **kwargs):
        if command == 'insult' and args:
            insultee = args
            return [(0, channel, self.get_insult(insultee.strip()))]

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
        return "%s, you %s %s %s." % (insultee,
                                     self.shake_insults[0][randint(0, length)],
                                     self.shake_insults[1][randint(0, length)],
                                     self.shake_insults[2][randint(0, length)])
    def shakestring(self):
        return """artless             base-court          apple-john
bawdy               bat-fowling         baggage
beslubbering        beef-witted         barnacle
bootless            beetle-headed       bladder
churlish            boil-brained        boar-pig
cockered            clapper-clawed      bugbear
clouted             clay-brained        bum-bailey
craven              common-kissing      canker-blossom
currish             crook-pated         clack-dish
dankish             dismal-dreaming     clotpole
dissembling         dizzy-eyed          coxcomb
droning             doghearted          codpiece
errant              dread-bolted        death-token
fawning             earth-vexing        dewberry
fobbing             elf-skinned         flap-dragon
froward             fat-kidneyed        flax-wench
frothy              fen-sucked          flirt-gill
gleeking            flap-mouthed        foot-licker
goatish             fly-bitten          fustilarian
gorbellied          folly-fallen        giglet
impertinent         fool-born           gudgeon
infectious          full-gorged         haggard
jarring             guts-griping        harpy
loggerheaded        half-faced          hedge-pig
lumpish             hasty-witted        horn-beast
mammering           hedge-born          hugger-mugger
mangled             hell-hated          joithead
mewling             idle-headed         lewdster
paunchy             ill-breeding        lout
pribbling           ill-nurtured        maggot-pie
puking              knotty-pated        malt-worm
puny                milk-livered        mammet
qualling            motley-minded       measle
rank                onion-eyed          minnow
reeky               plume-plucked       miscreant
roguish             pottle-deep         moldwarp
ruttish             pox-marked          mumble-news
saucy               reeling-ripe        nut-hook
spleeny             rough-hewn          pigeon-egg
spongy              rude-growing        pignut
surly               rump-fed            puttock
tottering           shard-borne         pumpion
unmuzzled           sheep-biting        ratsbane
vain                spur-galled         scut
venomed             swag-bellied        skainsmate
villainous          tardy-gaited        strumpet
warped              tickle-brained      varlot
wayward             toad-spotted        vassal
weedy               unchin-snouted      whey-face
yeasty              weather-bitten      wagtail"""

