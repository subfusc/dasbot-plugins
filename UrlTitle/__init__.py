# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Herman Torjussen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://gnu.org/licenses/>.

from random import randint
import htmlentitydefs
import BeautifulSoup
import urllib2
import urlparse
import re

#### Taken from Stack Overflow
#### Distributed under CC: Attributed Share Alike
#### user: bobince
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )
#### End taken from Stack Overflow

class Plugin(object):

    def __init__(self):
        self.url_regex = r"https?://(?!play.spotify.com)([^.]+.[^.]+)(.[^.]+)*(/([^/]+/)*([^.]+.[^?]+)?([?]\S+)?)?"
        self.blank_regex = r"\s+"
        self.MAXLINEWIDTH = 79
        self.ure = re.compile(self.url_regex)
        self.titlesub = re.compile(self.blank_regex)

    def listen(self, msg, channel, **kwargs):
        chanurl = self.ure.search(msg)
        if chanurl:
            title = self.urltitle(chanurl.group())
            if title:
                return [(1, channel, title[:self.MAXLINEWIDTH])]

    def urltitle(self, url):
        url = url.decode("utf-8")
        url = iriToUri(url)
        req = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
        try:
            page_content = urllib2.urlopen(req, timeout=3)
            page_soup = BeautifulSoup.BeautifulSoup(page_content)
        except urllib2.URLError:
            return None
        except:
            print "UrlTitle. Other error"
            return None
        title = None
        if page_soup.title and page_soup.title.string:
            title = page_soup.title.string.strip()
            title = self.titlesub.sub(" ", title)
            title = self.unescape(title).encode("utf-8")
        return title ? title.replace('Trump', 'Drumpf') : None


    """
    Fredrik Lundh, 2006
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)
