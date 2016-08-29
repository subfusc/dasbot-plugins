# -*- coding: utf-8 -*-
import GlobalConfig as conf
import copy
import ConfigParser  # remove
import datetime
import time
import dateutil.parser
from dateutil.tz import tzutc
import feedparser
from collections import OrderedDict
# import re
import os
# import sys #remove

FREQUENCY = 120  # seconds


class Plugin(object):
    """
    TODO
    - Check if computer can send to channel
    """

    def __init__(self, **kwargs):
        self.latestfeed = {}  # feed: {updated, entries}
        self.cronjobs = []
        self.new_job = kwargs['new_job']
        self.del_job = kwargs['del_job']
        self.feeds = {}
        for sec in kwargs['config'].sections():
            self.feeds[sec] = OrderedDict()
            for it in kwargs['config'].items(sec):
                self.feeds[sec][it[0]] = it[1]
        print self.feeds
        # self._check_cron()
        tmp = self.new_job((time.time() + 5, self._check_cron, []))
        self.cronjobs.append(tmp)

    def _del_jobs(self, **kwargs):
        for job in self.cronjobs:
            kwargs['del_job'](job)

    def _add_feed(self, key, feed, channel, from_nick):
        if not channel[1:] in self.feeds:
            self.feeds[channel[1:]] = {}
        self.feeds[channel[1:]][key] = feed
        self._write_config()
        return [(1, channel, from_nick, "feed added")]

    def _del_feed(self, key, channel, from_nick):
        self.feeds[channel[1:]].pop(key, None)
        self._write_config()
        return [(1, channel, from_nick, "feed deleted")]

    def _list_feeds(self, channel, from_nick):
        feeds = self.feeds.get(channel)
        if feeds:
            rlst = []
            for k, v in feeds.items():
                rlst.append([(1, channel, from_nick, "{}: {}".format(k, v))])
            return rlst
        else:
            return [(1, channel, from_nick, "No feeds for this channel")]

    def _write_config(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cfg = ConfigParser.RawConfigParser()
        for sec in self.feeds.keys():
            cfg.add_section(sec)
            for key, feed in self.feeds[sec].items():
                cfg.set(sec, key, feed)
        with open(dir_path + '/plugin.cfg', 'w') as f:
            cfg.write(f)

    def _check_cron(self):
        print "=== check cron ==="
        self.now = (datetime.datetime.now(tzutc()))
        return_lst = []
        for channel, feeds_c in self.feeds.items():
            print "=== feeds_c", feeds_c
            for key, feed in feeds_c.items():
                print '=== ', key, feed
                ltst = self._check(feed, channel)
                #print entries
                if ltst == -1:
                    print "-1"
                else:
                    entries = ltst['entries']
                    for entry in entries:
                        print entry['title']
                        return_lst.append((0, "#" + channel, u"[{}] {} {}".format(key, entry['title'], entry['link']).encode('utf-8')))
        self.cronjobs.append(self.new_job((time.time() + FREQUENCY, self._check_cron, [])))
        print return_lst
        return return_lst

    def _check(self, feed, channel):
        print "feed: ", feed, '.'
        latest = self.latestfeed.get(feed)
        if not latest:
            latest = {'updated': self.now - datetime.timedelta(minutes=3)} # to datetime - 1h
        if latest['updated'] == self.now:
            # feed already updated
            return latest
        print "feed: ", feed
        d = feedparser.parse(feed)
        if not d.feed:
            return -1
        try:
            ddate = dateutil.parser.parse(d.feed.updated)
        except:
            ddate = (self.now - datetime.timedelta(hours=12))
        if ddate > latest.get('updated'):
            print "hit"
            last = copy.deepcopy(latest)
            latestupdated = latest['updated']
            latest['entries'] = []
            for entry in d.entries:
                edate = dateutil.parser.parse(entry.updated)
                if (edate > latestupdated and
                        not self._match(entry, last)):
                    latest['entries'].append(entry)
            latest['updated'] = self.now
            self.latestfeed[feed] = latest
        self.latestfeed['updated'] = self.now
        if 'entries' not in latest:
            latest['entries'] = []
        return latest

    def _match(self, entry, last):
        if not last.get('entries'):
            return False
        for e in last.get('entries'):
            if e.title == entry.title:
                return e
        return False

    def help(self, command, args, channel, **kwargs):
        if command == 'delfeed':
            return [(1, kwargs['from_nick'], conf.COMMAND_CHAR + command + " key [channel]")]
        if command == 'addfeed':
            return [(1, kwargs['from_nick'], conf.COMMAND_CHAR + command + " key feed [channel]")]

    def listen(self, msg, channel, **kwargs):
        pass

    def cmd(self, command, args, channel, **kwargs):
        if command == 'listfeeds':
            if args:
                return _list_feeds(args, kwargs['from_nick'])
            return _list_feeds(channel, kwargs['from_nick'])
            
        if command == 'delfeed':
            args = args.split()
            if len(args) >= 2:
                if args[1][1] != '#':
                    args[1] = '#' + args[1]
                return self._del_feed(args[0], args[1], kwargs['from_nick'])
            return self._del_feed(args[0], channel, kwargs['from_nick'])
        if command == 'addfeed':
            args = args.split()
            if len(args) < 2:
                return [(0, channel, kwargs['from_nick'], 'todo usage')]
            if len(args) >= 3:
                print args
                #if args[2][0] != '#':
                #    args[2] = '#' + args[2]
                return self._add_feed(args[0], args[1], args[2],
                                      kwargs['from_nick'])
            return self._add_feed(args[0], args[1], channel,
                                  kwargs['from_nick'])
        if command == 'deljobs':
            n = len(self.cronjobs)
            self._del_jobs(**kwargs)
            return [(0, channel, kwargs['from_nick'], 'deleted', n, 'jobs.')]

if __name__ == '__main__':
    print('configparser')
    config = ConfigParser.ConfigParser()
    config.read("plugin.cfg")
    p = Plugin(config=config)
    p.feeds['foobot'] = ['foo']
    print p.feeds
    p._write_config()
    #print(p.cmd('', None, '#iskbot'))
