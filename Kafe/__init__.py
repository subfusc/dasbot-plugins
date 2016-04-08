# -*- coding: utf-8 -*-
from Kafe import Kafe
#from GlobalConfig import *

class Plugin(object):

    def __init__(self):
        self.cafe_api = Kafe()

    def response_for_cafe(self, channel, nick, cafe):
        dinnars = self.cafe_api.dinners_for(cafe)
        response = []
        for category in dinnars:
            if category['category'] == u'pris': continue
            for dish in category['dishes']:
                dish = dish.split('Allergener')[0].split(':')[-1].encode('utf-8')
                response.append((0, channel, nick, '[{}] {}'.format(category['category'].encode('utf-8'), dish)))

        return response

    def cmd(self, command, args, channel, **kwargs):
        if command == 'middag':
            if args and len(args) > 0:
                cafes = self.cafe_api.cafes(args)
                cafes = [c.encode('utf-8') for c in cafes]
                if len(cafes) == self.cafe_api.number_of_cafes:
                    return [(0, channel, kwargs['from_nick'], 'Tilgjengelige kafeer: {}'.format(cafes))]
                elif len(cafes) == 1:
                    return self.response_for_cafe(channel, kwargs['from_nick'], cafes[0])
                else:
                    return [(0, channel, kwargs['from_nick'], 'Mente du en av disse: {}'.format(cafes))]
            else:
                return self.response_for_cafe(channel, kwargs['from_nick'], 'informatikk')


if __name__ == '__main__':
    p = Plugin()
    print p.cmd('middag', None, 'iskbot', from_nick='foo')
    print p.cmd('middag', 'fr', 'iskbot', from_nick='foo')
    print p.cmd('middag', 'i', 'iskbot', from_nick='foo')
