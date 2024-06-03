from django.db import models

# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=300)
    image = models.ImageField(upload_to='service/')

    @property
    def image_url(self):
        url = self.image.url
        if url is None:
            url = ""
        return url

    def __str__(self):
        return self.title


class Aboutus(models.Model):
    title = models.CharField(max_length=50)
    number = models.IntegerField()
    image = models.ImageField(upload_to='service/')

    @property
    def image_url(self):
        url = self.image.url
        if url is None:
            url = ""
        return url

    def __str__(self):
        return self.title
