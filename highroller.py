# -*- coding: utf-8 -*-

import requests
from furl import furl
import os

KEYWORD_EXCLUDE_END = '<!-- highroller: exclude end -->'
KEYWORD_EXCLUDE_START = '<!-- highroller: exclude start -->'

KEYWORD_ADDITIONAL_END = '<!-- highroller: additional end -->'
KEYWORD_ADDITIONAL_START = '<!-- highroller: additional start -->'

KEYWORD_AURL_START = 'href="'
KEYWORD_AURL_END = '"'


class Highroller:
    def __init__(self):
        self.domain = ''
        self.additional_sites = []



    def register_additional_site(self, url):
        """ Please overwrite this function to get custom url handling
        """
        if url[0] == '/':
            outputname = os.path.join("/static/", url[1:])        
        else:
            outputname = os.path.join("/static/", url)
        
        if not  (url, outputname) in self.additional_sites:
            self.additional_sites.append((url, outputname))
            
        return outputname

    def _run_exclude(self, content_original):

        hit = True
        while hit:
            hit = False
            occurence_start = content_original.find(
                KEYWORD_EXCLUDE_START)
            if not occurence_start == -1:
                occurence_end = content_original.index(
                    KEYWORD_EXCLUDE_END)
                content_original = content_original[:occurence_start] + \
                    content_original[occurence_end + len(KEYWORD_EXCLUDE_END):]
                hit = True
        return content_original

    def _run_additional(self, content_original):
        hit = True
        while hit:
            hit = False
            occurence_start = content_original.find(
                KEYWORD_ADDITIONAL_START)
            if not occurence_start == -1:
                occurence_end = content_original.index(
                    KEYWORD_ADDITIONAL_END)
                # clean hit
                a_hit = content_original[occurence_start + len(
                    KEYWORD_ADDITIONAL_START):occurence_end]
                a1 = a_hit.find(KEYWORD_AURL_START)
                a2 = a_hit[a1 + len(KEYWORD_AURL_START):].find(KEYWORD_AURL_END)
                url = a_hit[a1 + len(KEYWORD_AURL_START):a1 + len(
                    KEYWORD_AURL_START) + a2]
                content_original = content_original[:occurence_start] + a_hit[:a1 + len(KEYWORD_AURL_START)] + self.register_additional_site(
                    url) + a_hit[a1 + len(KEYWORD_AURL_START) + a2:] + content_original[occurence_end + len(KEYWORD_ADDITIONAL_END):]
                hit = True
        return content_original

    def roll_site(self, element):
        ################################################################
        # get content
        ################################################################
        
        f = furl(self.domain)
        f.path = str(f.path) + element[0]
        target_url = f.url
        response = requests.get(target_url)
        content_original = response.content

        ################################################################
        # remove unused parts
        ################################################################
        content_original = self._run_exclude(content_original)
        ################################################################
        # rewrite links and find new pages
        ################################################################
        content_original = self._run_additional(content_original)
        ################################################################
        # write new content
        ################################################################
        

        if element[1][0] == '/':
            destination = os.path.join(os.path.dirname(__file__),element[1][1:])
        else:
            destination = os.path.join(os.path.dirname(__file__),element[1])
        
        with open(destination, 'w') as f:
            f.write(content_original)
        # write content here to element 1

if __name__ == '__main__':
    print "yeah"
    hr = Highroller()
    hr.domain = "http://localhost"
    #hr.additional_sites.append(("/", "index.html"))
    hr.register_additional_site("/index.html")
    for element in hr.additional_sites:
        print "------------roll------------"
        hr.roll_site(element)

    print hr.additional_sites
