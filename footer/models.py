from django.db import models

# Create your models here.


class Information(models.Model):
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    google_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.phone_number
