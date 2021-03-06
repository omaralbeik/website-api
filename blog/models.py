from django.db import models
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(is_published=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image_url = models.URLField(blank=True, null=True)
    cover_image_credit_badge = models.TextField(blank=True, null=True)
    summary = models.TextField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    text = MarkdownxField()
    is_published = models.BooleanField(default=False)
    date_published = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)

    objects = models.Manager()
    visible = PostManager()

    related = models.ManyToManyField('Post', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-is_published", "-date_published", "-date_created"]
