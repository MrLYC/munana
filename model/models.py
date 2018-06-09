# coding: utf-8

from django.db import models

from utils.num import convert_cn_number


class Article(models.Model):
    index = models.IntegerField()
    url = models.CharField()
    title = models.CharField()
    content = models.TextField()

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        if self.index == 0:
            self.index = convert_cn_number(self.title)
