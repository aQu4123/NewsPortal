from random import choices
from django.db import models
from django.contrib.auth.models import User
from news.resources import POSITIONS, news


class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        self.rating = (
            sum(post.rating * 3 for post in Post.objects.filter(author=self)) +
            sum(comment.rating for comment in Comment.objects.filter(user=self.user)) +
            sum(comment.rating for comment in Comment.objects.filter(post__author=self))
        )
        self.save()

class Category(models.Model):
    name = models.CharField(max_length = 64, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type = models.CharField(max_length = 2, choices = POSITIONS, default = news)
    date_in = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 64)
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '. . .'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField()
    date_in = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
