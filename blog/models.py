from django.db import models

from user.models import Member


# from user.models import User


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=256, blank=True)
    content = models.TextField(blank=True)
    vis = models.BooleanField(default=True)
    member = models.ForeignKey(Member, models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog"
