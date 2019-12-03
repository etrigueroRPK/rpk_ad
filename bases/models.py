from django.db import models

from django.contrib.auth.models import User

class ClassModel(models.Model):
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    user_updated = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract=True