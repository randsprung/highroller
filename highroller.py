# -*- coding: utf-8 -*-

import requests
from furl import furl
import os, sys, shutil

KEYWORD_EXCLUDE_END = '<!-- highroller: exclude end -->'
KEYWORD_EXCLUDE_START = '<!-- highroller: exclude start -->'

KEYWORD_INCLUDE_END = '!-- highroller: include end -->'
KEYWORD_INCLUDE_START = '<!-- highroller: include start --'

KEYWORD_ADDITIONAL_END = '<!-- highroller: additional end -->'
KEYWORD_ADDITIONAL_START = '<!-- highroller: additional start -->'

KEYWORD_AURL_START = 'href="'
KEYWORD_AURL_END = '"'


class Highroller:
    def __init__(self):
        self.domain = ''
        self.additional_sites = []
        self.inject_head = ''
        self.inject_body = ''
        self.output_dir = '/static/'

    def register_additional_site(self, url):
        """ Please overwrite this function to get custom url handling
        """
        if len(url) and url[0] == '/':
            outputname = os.path.join(self.output_dir, url[1:])
        elif url.startswith("http"):
            f = furl(url)
            outputname = os.path.join(self.output_dir, str(f.path)[1:])
        else:
            outputname = os.path.join(self.output_dir, url)
        if not outputname.endswith("html"):
            outputname = os.path.join(outputname, "index.html")
        if not (url, outputname) in self.additional_sites:
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

    def _run_include(self, content_original):

        hit = True
        while hit:
            hit = False
            occurence_start = content_original.find(
                KEYWORD_INCLUDE_START)
            if not occurence_start == -1:
                occurence_end = content_original.index(
                    KEYWORD_INCLUDE_END)

                #[:start] + [start + len(start):end] + [end + len(end):]
                content_original = content_original[:occurence_start] + \
                    content_original[occurence_start + len(KEYWORD_INCLUDE_START):occurence_end] + \
                    content_original[occurence_end + len(KEYWORD_INCLUDE_END):]
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
                a2 = a_hit[a1 + len(KEYWORD_AURL_START):
                           ].find(KEYWORD_AURL_END)
                url = a_hit[a1 + len(KEYWORD_AURL_START):a1 + len(
                    KEYWORD_AURL_START) + a2]
                
                url = url.replace('#', '/')
                url = url.replace('//', '/')

                content_original = content_original[:occurence_start] + a_hit[:a1 + len(KEYWORD_AURL_START)] + self.register_additional_site(
                    url) + a_hit[a1 + len(KEYWORD_AURL_START) + a2:] + content_original[occurence_end + len(KEYWORD_ADDITIONAL_END):]
                hit = True
        return content_original

    def _get_content(self, element):
        if element[0].startswith('http'):
            target_url = element[0]
        else:
            f = furl(self.domain)
            f.path = str(f.path) + element[0]
            target_url = f.url
        response = requests.get(target_url)#, headers=headers)
        return response.content

    def roll_site(self, element):
        content_original = self._get_content(element)
        content_original = content_original.replace(
            "</head>", self.inject_head + "</head>")
        content_original = content_original.replace(
            "</body>", self.inject_body + "</body>")
        content_original = self._run_include(content_original)
        content_original = self._run_exclude(content_original)
        content_original = self._run_additional(content_original)

        if element[1][0] == '/':
            destination = os.path.join(
                os.path.dirname(__file__), element[1][1:])
        else:
            destination = os.path.join(os.path.dirname(__file__), element[1])
        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        with open(destination, 'w') as f:
            f.write(content_original)
        return content_original

    def delete_site(self):
        folder = 'static'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                else:
                    shutil.rmtree(file_path)
            except Exception, e:
                print e

if __name__ == '__main__':
    hr = Highroller()
    hr.domain = "http://localhost"
    hr.inject_head = "<!-- headinject -->"
    hr.inject_body = "<!-- bodyinject -->"
    hr.register_additional_site("/index.html")
    for element in hr.additional_sites:
        print "roll: {0}".format(element[0])
        hr.roll_site(element)
