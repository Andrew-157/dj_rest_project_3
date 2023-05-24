from django.db import models
from store.validators import validate_file_size


class Category(models.Model):
    title = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='products')
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='store/images',
                              null=False, validators=[validate_file_size])

    def __str__(self):
        return self.title
