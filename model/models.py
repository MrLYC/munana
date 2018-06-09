# coding: utf-8

from django.db import models


class Article(models.Model):
    index = models.IntegerField()
    url = models.TextField()
    title = models.TextField()
    content = models.TextField()

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

    def __cmp__(self, other):
        return cmp(self.index, other.index)

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index