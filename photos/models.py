from django.db import models

# Create your models here.


class Slider(models.Model):
    pass


class Banner(models.Model):
    banner_man = models.ImageField(upload_to="Banner/")
    banner_women = models.ImageField(upload_to="Banner/")
    banner = models.ImageField(upload_to="Banner/")

    def __str__(self):
        return "Banner"

    @property
    def image_man_url(self):
        url = self.banner_man.url
        if url is None:
            url = ""
        return url

    @property
    def image_women_url(self):
        url = self.banner_women.url
        if url is None:
            url = ""
        return url

    @property
    def image_banner_url(self):
        url = self.banner.url
        if url is None:
            url = ""
        return url


class BaseInstagram(models.Model):
    base_instagram = models.CharField(
        max_length=9, default='Instagram', editable=False)

    def __str__(self):
        return "Instagram"


class Instagram(models.Model):
    instagram = models.ForeignKey(
        BaseInstagram, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="instagram/", null=True)

    @property
    def image_url(self):
        """this function check if it image is none or not."""

        url = self.image.url
        if url is None:
            url = ""
        return url

    def __str__(self):
        return 'Instagram'
