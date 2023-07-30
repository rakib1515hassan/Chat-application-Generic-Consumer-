from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()





# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Chat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.content

