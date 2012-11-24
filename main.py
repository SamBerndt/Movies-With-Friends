#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import httplib
from xml.dom.minidom import parseString

class MainHandler(webapp2.RequestHandler):
    def get(self):
        zip = self.request.get("zip")
        conn = httplib.HTTPSConnection("www.fandango.com")
        conn.request("GET","/rss/moviesnearme_"+zip+".rss")
        r = conn.getresponse()
        fandangoresponce = r.read()
        dom = parseString(fandangoresponce)
        theatres = dom.getElementsByTagName("item")
        movieList = {}
        for theatre in theatres:
            theatreName = theatre.getElementsByTagName("title")[0].childNodes[0].data
            moviexml = theatre.getElementsByTagName("description")[0].childNodes[0].data
            movies = parseString("<movies>" + moviexml.replace("&","&amp;") + "</movies>").getElementsByTagName("li")
            for movie in movies:
                aElement = movie.getElementsByTagName("a")[0]
                moviename = aElement.firstChild.data
                movielinklink = aElement.getAttribute("href")
                path = movielinklink.split("/")
                movieId = path[3].split("_")[1]

                if movieId in movieList:
                    movieList[movieId]["theatre"].append({"name": theatreName})
                else:
                    movieList[movieId] = { "name": moviename, "link": movielinklink, "theatre": [{"name": theatreName}]}

        output = ""
        for movieId in movieList:
            output = output + "<p><a href=\"" + movieList[movieId]["link"]+"\">" + movieList[movieId]["name"] + "</a><ul>"
            for theatre in movieList[movieId]["theatre"]:
                output = output + "<li>" + theatre["name"]+ "</li>"
            output = output + "</ul></p>"


        self.response.write(output)




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
