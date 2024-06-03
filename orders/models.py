from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from store.models import Product, Variation

# Create your models here.


class Order(models.Model):
    STATUS = (
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    order_note = models.TextField()
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(
        max_length=50, choices=STATUS, default='Processing')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
