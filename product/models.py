from django.db import models
from common.models import BaseModel
from users.models import CustomUser


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def products_count(self):
        return self.product_set.count()


class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=((i, '* ' * i) for i in range(1, 6)))  # от 1 до 5
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    def __str__(self):
        return self.text[:30]
