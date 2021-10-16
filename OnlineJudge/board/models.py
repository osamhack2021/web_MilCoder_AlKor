from django.db import models

from account.models import User
from problem.models import Problem
from utils.models import RichTextField

class Article(models.Model):
    title = models.TextField()
    content = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "board_article"
        ordering = ("-create_time",)


class Comment(models.Model):
    content = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        db_table = "board_comment"
        ordering = ("-create_time",)
