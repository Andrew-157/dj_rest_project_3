from django.db import models
from django.template.defaultfilters import slugify
from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Ingredient(models.Model):
    MILLILITRES = 'ml'
    MILLIGRAMS = 'mg'
    OUNCES = 'oz'
    LITRES = 'l'
    GRAMS = 'gm'
    UNITS_OF_MEASUREMENT = [
        (MILLILITRES, 'millilitres'),
        (MILLIGRAMS, 'milligrams'),
        (OUNCES, 'ounces'),
        (LITRES, 'litres'),
        (GRAMS, 'grams')
    ]
    name = models.CharField(max_length=155)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    units_of_measurement = models.CharField(max_length=2,
                                            choices=UNITS_OF_MEASUREMENT, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes', null=True)
    title = models.CharField(max_length=155, unique=True)
    instructions = models.TextField()
    slug = models.SlugField(max_length=155, unique=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
