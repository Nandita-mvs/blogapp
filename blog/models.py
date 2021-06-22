from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Author(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null="true", blank="true")
    def __str__(self):
        return f'{self.user}'

class Post(models.Model):
    title=models.CharField(max_length=250)
    slug=models.SlugField(null=True,blank=True)
    body_text=RichTextUploadingField(null=True)
    pub_date=models.DateTimeField(auto_now_add=True)
    author=models.ManyToManyField(Author)

    def __str__(self):
		    return self.title

    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.title, allow_unicode=True)           # add this
        super().save(*args, **kwargs) 

