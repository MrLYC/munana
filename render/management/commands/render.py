# coding: utf-8
import json

from django.template.loader import get_template
from django.core.management.base import BaseCommand

from model.models import Article


def json_to_articles(path):
    for line in open(path, "r"):
        if line:
            params = json.loads(line)
            yield Article(**params["result"])


class Command(BaseCommand):
    help = 'render result'

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')
        parser.add_argument(
            '--without_title', action='store_true', default=False)
        parser.add_argument('--sort', action='store_true', default=False)

    def handle(self, *args, **options):
        template = get_template("render/render_article.tpl")
        articles = json_to_articles(options["input"])
        with open(options["output"], "wt") as fp:
            for article in articles:
                data = options.copy()
                data["article"] = article
                fp.write(template.render(data))
