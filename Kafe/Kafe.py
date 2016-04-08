# -*- coding: utf-8 -*-
import urllib2
import re
import json

class Kafe(object):

    def __init__(self):
        self.url = 'http://api.desperate.solutions/dagens/'
        self._cafes = json.load(urllib2.urlopen(self.url))

    def number_of_cafes(self):
        return len(self._cafes)

    def cafes(self, prefix):
        if prefix:
            return [a for a in self._cafes.keys() if a.startswith(prefix)]
        else:
            return self._cafes

    def dinners_for(self,cafename):
        return json.load(urllib2.urlopen(self._cafes[cafename]))['cafeteria']

if __name__ == "__main__":
    test = Kafe()
    print test.cafes('sv')
    print test.cafes('fr')
    print test.dinners_for(test.cafes('fr')[0])
    print test.cafes('i')
    print test.number_of_cafes() == test.cafes('i')
