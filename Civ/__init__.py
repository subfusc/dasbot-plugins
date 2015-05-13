# -*- coding: utf-8 -*- 
# Copyright (C) 2015 Trond Thorbjørnsen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Notifications from civ server.
# Checks url for updates, notifies irc channel.
# 
# 
# Example of script to update web server on civ server:
# 
# inotifywait -m ~/ -e create --format "%f %T" --timefmt "%c" | \            
#  while read line
#  do
#  echo $line > log.txt
#  done

from GlobalConfig import *
import re
import codecs
import IRCFonts
import urllib2
import time

class Plugin(object):

    def __init__(self, **kwargs):
        self.last = ""
        self.sleeptime = 30
        self.jobs = []

    def help(self, command, args, channel, **kwargs):
        if command == 'civ-log-start':
            msg = [(1, kwargs['from_nick'], "Start notifikasjon fra civ-server")]
            msg.append((1, kwargs['from_nick'], "!civ-log-start [url]"))
            return msg
        if command == 'civ-log-stop':
            msg = [(1, kwargs['from_nick'], "Stop notifikasjon fra civ-server")]
            return msg
        if command == 'all':
            return [(1, kwargs['from_nick'], "Civ: civ-log-start, civ-log-stop")]

    def cmd(self, command, args, channel, **kwargs):
        if command == "civ-log-start":
            if args:
                self.url = args
            else:
                return [(0, channel, kwargs['from_nick'], "No civ-log url given.")]
            self.channel = channel
            self.run = True
            kwargs['new_job']((time.time() + self.sleeptime, self.check_civlog, [kwargs['new_job']]))
            return [(0, channel, kwargs['from_nick'], "civ-log checker started")]
        if command == "civ-log-stop":
            self.run = False
            return [(0, channel, kwargs['from_nick'], "civ-log checker stopped")]

    def check_civlog(self, new_job):
        if not self.run:
            return
        cur = self.civlog()
        if cur != self.last:
            new_job((time.time() + self.sleeptime, self.check_civlog, [new_job]))
            self.last = cur
            tmp = "Ny runde: {}".format(cur)
            return [(0, self.channel, tmp)]#
        new_job((time.time() + self.sleeptime, self.check_civlog, [new_job]))
        #return [(0, self.channel, 'tralala')]
            
    def civlog(self):
        f = urllib2.urlopen(self.url)
        s = f.read()
        f.close()
        return s

