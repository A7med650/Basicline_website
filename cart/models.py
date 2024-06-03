from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    # is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.product.sale_price:
            return self.product.sale_price*self.quantity
        else:
            return self.product.price*self.quantity

    def __str__(self):
        return self.product.product_name
