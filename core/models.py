from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # Relación con el usuario
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
