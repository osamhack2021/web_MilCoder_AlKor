from django.db import models

from account.models import User
from utils.models import RichTextField

class Article(models.Model):
    title = models.TextField(null=False)
    content = RichTextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    # TODO: 유저가 삭제되면?
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "board_article"
        ordering = ("-create_time",)
