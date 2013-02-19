# -*- coding: utf-8 -*-
import copy
from rosetta.polib import pofile
from rosetta.poutil import find_pos
from django.utils.translation import to_locale

# Holds a catalog of locale's in memory without fallback messages
_catalogs = {}


def get_language_catalog(language):
    """

    @param language:
    @type language: str
    @return:
    """
    locale = to_locale(language)
    catalog = _catalogs.get(locale, None)
    if catalog is not None:
        return catalog

    files = find_pos(locale, third_party_apps=True)
    catalog = copy.deepcopy(pofile(files[0]))
    print "Language= ", repr(locale), repr(files), ", "

    # Join the other po files to the original
    for i in range(1, len(files)):
        deep = copy.deepcopy(pofile(files[i]))
        print "Path = ", files[i]
        for entry in deep:
            entry.pfile = files[i]
            catalog.append(entry)

    catalog.dict = dict((e.msgid, e) for e in catalog)
    _catalogs[locale] = catalog

    #print "Catalog: ", repr(catalog)
    #print "Dict: ", repr(catalog.dict)
    #print "Fetch: ", repr(catalog.dict['"You don’t need to grow a beard to become a Viking."'])
    #return {}
    return catalog


def encode(message):
    """

    @param message:
    @type message: str
    @return:
    """
    try:
        return message.decode().encode('utf-8')
    except UnicodeEncodeError:
        return message.encode('utf-8')


def escape(message):
    """

    @param message:
    @type message: str
    @return:
    """
    #return message.replace('<', '&lt;').replace('>', '&gt;')
    return message.replace('&', '&amp;') \
        .replace('<', '&lt;') \
        .replace('>', '&gt;') \
        .replace('"', '&quot;') \
        .replace("'", '&#39;')