from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe


class Ip (models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    views = models.ManyToManyField(Ip, related_name="post_views", blank=True)
    #likes
    #comments

    def __str__(self):
        return f'[{self.title}] - [{self.date}] user - [{self.user}]'

    def get_absolute_url(self):
        return reverse('single_news', kwargs={'pk':self.pk})

    def total_views(self):
        return self.views.count()


    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['date']



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='img/user_icon.png', upload_to='img/avatars/%Y/%m/%d')

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment [{self.body}] by [{self.name}]'

    def total_Comments(self):
        return Post.comments.count()

