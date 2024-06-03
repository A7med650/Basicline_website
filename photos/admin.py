from django.contrib import admin
from .models import BaseInstagram, Instagram, Banner

# Register your models here.


class InstagramInline(admin.StackedInline):
    model = Instagram
    extra = 2
    max_num = 20


class BaseInstagramAdmin(admin.ModelAdmin):
    model = BaseInstagram
    inlines = [InstagramInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if BaseInstagram.objects.count() > 0:
            return False
        return super().has_add_permission(request)


class BannerAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Banner.objects.count() > 0:
            return False
        return super().has_add_permission(request)


admin.site.register(BaseInstagram, BaseInstagramAdmin)

admin.site.register(Banner, BannerAdmin)
