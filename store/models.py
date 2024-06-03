from django.db import models
from category.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.

variation1 = None
variation2 = None


class Product(models.Model):
    FLAG = (
        ('New', 'New'),
    )

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, max_length=800)
    price = models.FloatField()
    discount = models.IntegerField(default=0, validators=[MinValueValidator(
        0), MaxValueValidator(100)])
    sale_price = models.FloatField(blank=True, null=True, editable=False)
    flag = models.CharField(max_length=20, choices=FLAG, blank=True, null=True)
    first_image = models.ImageField(upload_to='photos/products', null=True)
    second_image = models.ImageField(upload_to='photos/products', null=True)
    is_man = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def average_review(self):
        reviews = ReviewRating.objects.filter(
            status=True, product=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(
            status=True, product=self).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    @property
    def first_image_url(self):
        """this function check if it image is none or not."""

        url = self.first_image.url
        if url is None:
            url = ""
        return url

    @property
    def second_image_url(self):
        """this function check if it image is none or not."""

        url = self.second_image.url
        if url is None:
            url = ""
        return url


def product_pre_save(sender, instance, *args, **kwargs):
    if instance.discount > 0:
        instance.sale_price = (instance.discount/100)*instance.price
        instance.sale_price = instance.price - instance.sale_price
    elif instance.discount == 0:
        instance.sale_price = None


pre_save.connect(product_pre_save, Product)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color')

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size')


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='store/products')

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

    def image_url(self):
        url = self.image.url
        if url is None:
            url = ""
        return url

    def __str__(self):
        return self.product.product_name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name


class Compositions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Composition'
        verbose_name_plural = 'Compositions'

    def __str__(self):
        return self.product.product_name
