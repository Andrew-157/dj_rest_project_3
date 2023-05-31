from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from users.models import CustomUser
from recipes.validators import validate_file_size


class Category(models.Model):
    title = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=155, unique=True)
    instructions = models.TextField()
    slug = models.SlugField(max_length=155, unique=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT, related_name='recipes')
    published = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

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
    slug = models.SlugField(max_length=155, blank=True)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    units_of_measurement = models.CharField(max_length=2,
                                            choices=UNITS_OF_MEASUREMENT, null=True)
    recipe = models.ForeignKey(
        Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Ingredient, self).save(*args, **kwargs)


class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='recipes/images/', validators=[validate_file_size])

    class Meta:
        ordering = ['id']


class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        CustomUser, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['published']
