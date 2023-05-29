from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
