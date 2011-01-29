#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import urllib2
from HTMLParser import HTMLParser
from urlparse import urlparse

class ExtractTextLinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ""
        self.body = False
        self.pre = False
        self.dt = False
        self.dd = False
        self.file = None
        self.isWrite = False

    def filewrite(self, data):
        if self.isWrite:
            self.file.write(data)
            self.file.write("\n")

    def fileopen(self, filename):
        self.fileclose()
        self.file = open("_rst/"+filename+".rst", "w")
    def fileclose(self):
        if self.file:
            self.file.close()


    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = True
        if self.body:
            # if tag == "h1":
            #     print ""
            if tag == "pre":
                self.pre = True
            if tag == "dt":
                self.dt = True
            if tag == "dd":
                self.dd = True


    def handle_endtag(self, tag):
        if self.body:
            if tag == "h1" or tag == "h2" or tag == "h3":
                if tag == "h1":
                    chapter = self.text.lower()

                    if chapter.find("chapter") == 0:
                        fields = self.text.split(" ")
                        filename = fields[0].lower()
                        filename += fields[1]
                        if fields[1]!="1":
                            self.fileopen(filename)
                            self.isWrite = True
                    else:
                        self.isWrite = False

                    self.filewrite( ".. image:: biopython.jpg" )
                    self.filewrite("")
                    self.filewrite( ".. Overview")
                    self.filewrite("")
                self.filewrite( ".. index::")
                if tag == "h1":
                    self.filewrite( "   single: " + self.text + ";" + self.text)
                else:
                    self.filewrite( "   pair: " + self.text + ";" + self.text)
                self.filewrite("")
                self.filewrite( self.text)
                if tag == "h1":
                    self.filewrite( "="*len(self.text) )
                else:
                    self.filewrite( "-"*len(self.text) )
                self.filewrite("")
                self.text = ""
            elif tag == "p":
                if self.text != "":
                    self.filewrite( ".. " + self.text)
                    self.filewrite("")
                    self.filewrite( self.text)
                    self.filewrite("")
                self.text = ""

            elif tag == "pre":
                self.filewrite( ".. code-block:: python")
                self.filewrite("")
                self.filewrite( "    "+ self.text.replace("\n","\n    "))
                self.filewrite("")
                self.pre = False
                self.text = ""
            if tag == "dt":
                self.filewrite( "**"+self.text+"**")
                self.filewrite("")
                self.dt = False
                self.text = ""
            if tag == "dd":
                self.filewrite( "    "+ self.text.replace("\n","\n    "))
                self.filewrite("")
                self.dd = False
                self.text = ""


    def handle_data(self, data):
        if self.body:
            if not self.pre:
                if len(data) != 1:
                    data = data.replace("\n"," ")
                else:
                    data = data.replace("\n","")
            if data != "" and data != "\n":

                self.text += data
                #print "["+data+"]"

    def handle_charref(self, ref):
        if self.body:
            if ref == "XA0":
                self.text += " "
            if ref == "X2018":
                self.text += "‘"
            if ref == "X2019":
                self.text += "’"
            if ref == "X201C":
                self.text += "“"
            if ref == "X201D":
                self.text += "”"
            #print ref

    def handle_entityref(self, name):
        if self.body:
            if name == "amp":
                self.text += "&"
            if name == "nbsp":
                self.text += " "
            if name == "lt":
                self.text += "<"
            if name == "gt":
                self.text += ">"


def parse_biopython_tutorial(url):
    if os.path.exists("_rst"):
        shutil.rmtree("_rst")
    os.mkdir("_rst")
    response = urllib2.urlopen(url)
    parser = ExtractTextLinkParser()
    parser.feed(response.read())
    parser.close()

parse_biopython_tutorial("http://biopython.org/DIST/docs/tutorial/Tutorial.html")
