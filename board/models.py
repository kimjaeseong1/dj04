from tkinter import CASCADE
from django.db import models
from acc.models import User
from django.utils import timezone
# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="writer")
    content = models.TextField()
    pubdate = models.DateTimeField(default=timezone.now())
    likey = models.ManyToManyField(User, blank=True,related_name="likey") #x투표기능 유저와 n:n 관계

    def __str__(self):
        return self.subject
    
    def summary(self):
        if len(self.content) > 100:
            return f"{self.content[:100]}"
        return self.content
    
    def hot(self):
        if self.likey.count() >= 2:
            return True
        return False


class Reply(models.Model):
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.board}_{self.replyer}"