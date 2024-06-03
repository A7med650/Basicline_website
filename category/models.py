from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
