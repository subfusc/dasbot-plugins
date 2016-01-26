# -*- coding: utf-8 -*-
from urllib import urlopen
import re
import json
import time
import tinyurl

spotify_adr = r'\s*(https://play.spotify.com/([^/]+)/(\S+))\s*'
spotify_thing = r'\s*spotify:([^:]+):(\S+)\s*'

class Plugin:

    def __init__(self):
        self.spre = re.compile(spotify_adr)
        self.spt = re.compile(spotify_thing)
        self.spe = SpotifyExtract()

    def check_and_msg(self, channel, result):
        if result[0] != None and result[1] != None:
            return [(0, channel, "{a} by {b}, {c} ".format(a = result[1].encode('utf-8'), b = result[0].encode('utf-8'), c = tinyurl.create_one(self.spe.youtube_search(result[1].encode('utf-8'), result[0].encode('utf-8')))))]

    def listen(self, msg, channel, **kwargs):
        match = self.spre.search(msg)
        if match:
            return self.check_and_msg(channel, self.spe.rewrite_and_parse(match.group(2), match.group(3)))

        match = self.spt.search(msg)
        if match:
            return self.check_and_msg(channel, self.spe.rewrite_and_parse(match.group(1), match.group(2)))

class SpotifyExtract:

    def to_plural(self, string):
        "Yes, it is simpel. But will work for most cases. Update after need."
        return string + 's'

    def rewrite_and_parse(self, spotify_type, identifier):
        if ['album', 'track'].count(spotify_type) == 1:
            return self.parse_spotify("http://api.spotify.com/v1/%s/%s" % (self.to_plural(spotify_type), identifier))
        else:
            return [None, None]
        
    def parse_spotify(self, url):
        answer = json.loads(urlopen(url).read())
        return (', '.join(map(lambda a: a['name'], answer['artists'])), answer['name'])

    def youtube_search(self, title, artist):
        title = title.replace(" ", "+")
        artist = artist.replace(" ", "+").replace(",", "")
        return "http://www.youtube.com/results?search_query=%s+%s" % (title, artist)
