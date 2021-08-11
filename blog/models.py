from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import F

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    claps = models.PositiveSmallIntegerField(default=0)

    #method to update the publish_date (initially null) when user clicks publish
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #to show only comments by others that are approved by publisher
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    #redirecting url to post page itself after author publishes the post
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to='author'

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    #redirecting url to home page after user enters comment
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
