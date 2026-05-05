from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def products_count(self):
        return self.product_set.count()

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=((i, '* ' * i) for i in range(1, 6)))  # от 1 до 5
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    def __str__(self):
        return self.text[:30]