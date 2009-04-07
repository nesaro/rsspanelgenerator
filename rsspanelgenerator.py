#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of rsspanelgenerator.

#rsspanelgenerator is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#rsspanelgenerator is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with rsspanelgenerator.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright (c) 2009 Néstor Arocha Rodríguez"


import feedparser
import time
HOURS=128 
MAXTEXT=128

feeddic = { "twitter":"http://twitter.com/statuses/user_timeline/14784998.rss",
        "infosdv":"http://infosdv.blogspot.com/feeds/posts/default",
        "dopp":"http://nesaro.blogspot.com/feeds/posts/default",
        "adelinbackup-svn":"http://code.google.com/feeds/p/adelinbackup/svnchanges/basic",
        "gtol-svn":"http://code.google.com/feeds/p/gtol/svnchanges/basic"}
entrydic = {}

for feedtitle,feedaddress in feeddic.items():
    feedok = False
    feed = feedparser.parse(feedaddress)
    entrydic[feedtitle] = []
    for entry in feed.entries:
        if (time.time() - time.mktime(entry.updated_parsed)) < HOURS *3600:
            if entry.has_key("content"):
                entrydic[feedtitle].append((entry.updated_parsed, entry.title, entry.content[0]['value'], entry.link))
            elif entry.has_key("summary"):
                entrydic[feedtitle].append((entry.updated_parsed, entry.title, entry.summary, entry.link))
            else:
                raise TypeError
            feedok = True
    if not feedok:
        if feed.entries:
            entry = feed.entries[0]
            if entry.has_key("content"):
                entrydic[feedtitle].append((entry.updated_parsed, entry.title, entry.content[0]['value'], entry.link))
            elif entry.has_key("summary"):
                entrydic[feedtitle].append((entry.updated_parsed, entry.title, entry.summary, entry.link))
            else:
                raise TypeError


for entryname, entrylist in entrydic.items():
    if len(entrylist) > 0:
        result = u""
        result += "<li>"+ entryname + "<ul class=\"personalboxmini\">"
        for entry in entrylist:
            result += "<li>"
            result += "[" + str(entry[0][2]) + "/" + str(entry[0][1]) + "]"
            result += "<a href=\"" + entry[3] + "\">" + entry[1] + "</a>:"
            if entry[2] > MAXTEXT:
                result += entry[2][:MAXTEXT] + u"..."
            else:
                result += entry[2]
            result += "</li>"
        result += "</ul></li>"
        print result.encode('utf-8')
