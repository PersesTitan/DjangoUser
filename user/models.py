from datetime import datetime

from django.db import models


# Create your models here.
class Member(models.Model):
    login_id = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    create_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=5)
    name = models.TextField()
    # ...

    def __str__(self):
        return self.login_id

    class Meta:
        db_table = "member"
