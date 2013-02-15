# -*- coding: utf-8 -*-

import requests


KEYWORD_EXCLUDE_END = '<!-- highroller: exclude end -->'
KEYWORD_EXCLUDE_START = '<!-- highroller: exclude start -->'

KEYWORD_ADDITIONAL_END = '<!-- highroller: additional end -->'
KEYWORD_ADDITIONAL_START = '<!-- highroller: additional start -->'

KEYWORD_AURL_START = 'href="'
KEYWORD_AURL_END = '"'

additional_sites = []


def register_additional_site(url):
    outputname = "/static/" + url
    additional_sites.append((url, outputname))
    return outputname


def roll_site(element):
    target_url = domain + "/" + element[0]
    response = requests.get(target_url)
    content_original = response.content

    ################################################################
    # remove unused parts
    ################################################################

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

    ################################################################
    # rewrite links
    ################################################################

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
            content_original = content_original[:occurence_start] + a_hit[:a1 + len(KEYWORD_AURL_START)] + register_additional_site(
                url) + a_hit[a1 + len(KEYWORD_AURL_START) + a2:] + content_original[occurence_end + len(KEYWORD_ADDITIONAL_END):]
            hit = True
    print content_original
    # write content here to element 1

domain = "http://localhost"
additional_sites.append(("/", "index.html"))
for element in additional_sites:
    print "------------roll------------"
    roll_site(element)

print additional_sites
