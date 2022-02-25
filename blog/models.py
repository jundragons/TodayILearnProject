from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    id = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id + self.nickname