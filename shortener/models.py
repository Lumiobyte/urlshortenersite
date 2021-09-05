from django.db import models
from .utils import CreateShortenedURL

# Create your models here.

class ShortenedURL(models.Model):

    created = models.DateTimeField(auto_now_add = True)
    clicks = models.PositiveIntegerField(default = 0)
    longURL = models.URLField()
    shortURL = models.SlugField(max_length = 20, unique = True, blank = True)
    isVanity = models.BooleanField(default = False)

    class Meta:
        
        ordering = ['-created']

    def __str__(self):
        
        return f'{self.longURL} shortened to {self.shortURL}'

    def save(self, *args, **kwargs):

        if not self.shortURL:
            self.shortURL = CreateShortenedURL(self)

        super().save(*args, **kwargs)
