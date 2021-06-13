import logging
from os.path import dirname, join
import yaml
from typing import List, Dict, Any

from pelican import signals

log = logging.getLogger(__name__)


def get_authors() -> List[Dict[str, Any]]:
    FILENAME = join(dirname(dirname(dirname(__file__))), "authors.yaml")
    with open(FILENAME, "r") as f:
        authors = yaml.full_load(f)
    return authors


def test(content):
    # Get author information
    # Save to content.author object
    authors = get_authors()
    if content.authors:
        for author in content.authors:
            if author.name in authors:
                author.links = authors.get(author.name).get("links")
                log.warn(f'{authors.get(author.name).get("links")}')


def register():
    signals.content_object_init.connect(test)
