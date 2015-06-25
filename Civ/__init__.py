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
# inotifywait -m ~/ -e create modify --format "%f %T" --timefmt "%c" | \
#  while read line
#  do
#  if [[ $line == freeciv-T* ]]
#  then
#  echo $line > log.txt
#  fi
#  done

import re
import codecs
import urllib2
import time

class Plugin(object):

    def __init__(self, **kwargs):
        self.last = ""
        self.sleeptime = 30
        self.jobs = []
        self.longturn = {}

    def help(self, command, args, channel, **kwargs):
        if command == 'civ-log-start':
            msg = [(1, kwargs['from_nick'], "Start notifikasjon fra civ-server")]
            msg.append((1, kwargs['from_nick'], "!civ-log-start [url]"))
            return msg
        if command == 'civ-log-stop':
            msg = [(1, kwargs['from_nick'], "Stop notifikasjon fra civ-server")]
            return msg
        if command == 'longturn':
            msg = [(1, kwargs['from_nick'], "Start notifikasjon om nye turer i en longturn server. Trenger bare port nr for å regne ut turer.")]
            msg.append((1, kwargs['from_nick'], "!longturn <port>"))
            return msg
        if command == 'stop-longturn':
            msg = [(1, kwargs['from_nick'], "Stop notifikasjoner for en longturn server.")]
            msg.append((1, kwargs['from_nick'], "!stop-longturn <port>"))
            return msg
        if command == 'all':
            return [(1, kwargs['from_nick'], "Civ: civ-log-start, civ-log-stop, longturn, stop-longturn")]

    def cmd(self, command, args, channel, **kwargs):
        if command == "civ-log-start":
            if args:
                self.url = args
            else:
                return [(0, channel, kwargs['from_nick'], "Civ log url not given.")]
            self.channel = channel
            self.jobs.append(kwargs['new_job']((time.time() + self.sleeptime, self.check_civlog, [kwargs['new_job']])))
            return [(0, channel, kwargs['from_nick'], "civ-log checker started")]
        if command == "civ-log-stop":
            for i in self.jobs:
                kwargs['del_job'](i)
            return [(0, channel, kwargs['from_nick'], "civ-log checker stopped")]
        if command == 'longturn' and args:
            if args:
                try:
                    result = self.start_timer(channel, int(args), kwargs['new_job'])
                    if result:
                        return [(0, channel, kwargs['from_nick'], result)]
                except:
                    return [(0, channel, kwargs['from_nick'], "Not a port number.")]
        if command == 'stop-longturn' and args:
            if args:
                try:
                    kwargs['del_job'](self.longturn[channel][int(args)])
                    if self.longturn.has_key(channel):
                        chan = self.longturn[channel]
                        del(chan[int(args)])
                except:
                    return [(0, channel, kwargs['from_nick'], "Could not find job.")]


    def check_civlog(self, new_job):
        cur = self.civlog()
        if cur != self.last:
            self.jobs.append(new_job((time.time() + self.sleeptime, self.check_civlog, [new_job])))
            self.last = cur
            tmp = "Ny runde: {}".format(cur)
            return [(0, self.channel, tmp)]#
        self.jobs.append(new_job((time.time() + self.sleeptime, self.check_civlog, [new_job])))
        #return [(0, self.channel, 'no change')]

    def civlog(self):
        try:
            f = urllib2.urlopen(self.url)
            s = f.read()
            f.close()
            return s
        except:
            return self.last

    def time_untill_next_round(self, port):
        return 23*60*60 - (time.time() + port % 10 * (2 * 60 * 60)) % (23*60*60);

    def format_longturn_time(self, port):
        t = self.time_untill_next_round(port)
        return "Next round in {h} hours {m} minutes and {s} seconds.".format(h = int((t / (60 * 60))),
                                                                             m = int(((t / 60) % 60)),
                                                                             s =  int(t % 60))

    def new_round(self, channel, port, new_job):
        self.longturn[channel][port] = new_job((time.time() + self.time_untill_next_round(port), self.new_round, [channel, port, new_job]))
        return [(0, channel, "New round for longturn game on port {p}.".format(p = port))]

    def start_timer(self, channel, port, new_job):
        if self.longturn.has_key(channel):
            port_hash = self.longturn[channel]
            if port_hash.has_key(port):
                return self.format_longturn_time(port)
            else:
                port_hash[port] = new_job((time.time() + self.time_untill_next_round(port), self.new_round, [channel, port, new_job]))
        else:
            self.longturn[channel] = {port: new_job((time.time() + self.time_untill_next_round(port), self.new_round, [channel, port, new_job]))}

if __name__ == '__main__':
    p = Plugin()
    print(p.start_timer('foo',5121, lambda x: False ))
    print(p.start_timer('foo',5121, lambda x: False ))
