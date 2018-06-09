# coding: utf-8
import json
import bisect

from django.template.loader import get_template
from django.core.management.base import BaseCommand

from model.models import Article


def json_to_articles(path):
    for line in open(path, "r"):
        if line:
            params = json.loads(line)
            yield Article(**params["result"])


def sort_articles(articles):
    buf = []
    index = 0
    for a in articles:
        bisect.insort(buf, a)
        i = 0
        for i, article in enumerate(buf):
            if article.index - 1 <= index:
                yield article
                index = article.index
            else:
                break
        buf = buf[i:]

    for article in buf:
        yield article


class Command(BaseCommand):
    help = 'render result'

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')
        parser.add_argument(
            '--without_title', action='store_true', default=False)
        parser.add_argument(
            '--without_sort', action='store_true', default=False)

    def handle(self, *args, **options):
        template = get_template("render/render_article.tpl")
        articles = json_to_articles(options["input"])
        if not options["without_sort"]:
            articles = sort_articles(articles)
        with open(options["output"], "wt") as fp:
            for article in articles:
                print(article.title)
                data = options.copy()
                data["article"] = article
                fp.write(template.render(data))
