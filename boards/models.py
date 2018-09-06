from django.db import models

# Create your models here.
# import django defined user model
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

 # it convert to readable string that can be listed

    def __str__(self):
        return self.name
        
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('created_at').first()     

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)  

     # it convert to readable string that can be listed
 
    def __str__(self):
        return self.subject

#realed_name specifes the reverse relationship form Board to Topic
# one board can have many topics

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.CASCADE)

     # it convert to readable string that can be listed
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
 
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)