from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0, verbose_name='rating')

    def __str__(self):
        return f'{self.author}'

    def update_rating(self):
        post_rating = Post.objects.filter(post_author_id=self).values('post_rating')
        post_rating = sum(rate['post_rating'] for rate in post_rating) * 3
        comment_rating = Comment.objects.filter(comment_user_id=self.pk).values('comment_rating')
        comment_rating = sum(rate['comment_rating'] for rate in comment_rating)
        commentpost_rating = Post.objects.filter(post_author_id=self).values('comment__comment_rating')
        commentpost_rating = sum(rate['comment__comment_rating'] for rate in commentpost_rating)
        self.author_rating = post_rating + comment_rating + commentpost_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CategoryUser')

    def __str__(self):
        return f'{self.category}'

    def get_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    TYPES = [(article, 'статья'), (news, 'новость')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPES)
    post_time_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post_title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        prev = self.post_text
        if len(prev) > 124:
            return prev[:124 - len(prev)] + '...'
        else:
            return prev


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.category}'


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    comment_time_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.comment_text}'

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
