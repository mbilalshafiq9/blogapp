from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Category(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.TextField()
    status=models.IntegerField()
    timestamp=models.DateTimeField(default=now)
    
    def __str__(self):
        blog=self.title
        return blog

class Blog(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=120)
    content=models.TextField()
    image=models.ImageField(null=True, upload_to="images/")
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True,related_name='cat')
    author=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(default=now)
    
    def __str__(self):
        blog=self.title
        return blog

class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    comment=models.TextField()
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='blog')
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent=models.IntegerField(null=True)
    timestamp=models.DateTimeField(default=now)
    
    def __str__(self):
        comment=self.comment
        return comment

class Notificatino(models.Model):
    id=models.AutoField(primary_key=True)
    message=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent=models.IntegerField(null=True)
    timestamp=models.DateTimeField(default=now)
    
    def __str__(self):
        comment=self.comment
        return comment

        