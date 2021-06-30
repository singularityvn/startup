#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "doa"
SITENAME = "Singularity"
SITEURL = ""

PATH = "content"

TIMEZONE = "Asia/Ho_Chi_Minh"

DEFAULT_LANG = "vi"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGIN_PATHS = [
    "plugins",
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
}

STATIC_PATHS = [
    'extra',
    'images'
]

PLUGINS = ["extract_toc", "author", "simple_footnotes"]

DEFAULT_DATE_FORMAT = "%d-%m-%Y"

THEME = "themes/singularity"

DOCUTILS_SETTINGS = {
    "general": {
        "source-link": True,
    }
}
