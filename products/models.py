from django.db import models

from users.models import User

# Create your models here.
# models = таблица


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Продукт {self.name} | Категория {self.category}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity for basket in self])


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
