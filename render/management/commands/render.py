# coding: utf-8
import json
import bisect

from django.template.loader import get_template
from django.core.management.base import BaseCommand

from model.models import Article

from utils.num import convert_index


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


def sort_title(articles):
    def gen():
        for article in articles:
            article.index = convert_index(article.title)
            yield article

    return sort_articles(gen())


def sort_url(articles):
    return sorted(articles, key=lambda a: a.url)


class Command(BaseCommand):
    help = 'render result'

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')
        parser.add_argument('--without_title', action='store_true', default=False)
        parser.add_argument('--sort_title', action='store_true', default=False)
        parser.add_argument('--sort_url', action='store_true', default=False)
        parser.add_argument('--remove', nargs="+", default=[])

    def handle(self, *args, **options):
        template = get_template("render/render_article.tpl")
        articles = json_to_articles(options["input"])

        if options["sort_title"]:
            articles = sort_title(articles)
        elif options["sort_url"]:
            articles = sort_url(articles)

        with open(options["output"], "wt") as fp:
            for article in articles:
                data = options.copy()
                data["article"] = article
                fp.write(template.render(data))
