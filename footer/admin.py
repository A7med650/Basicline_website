from django.contrib import admin
from .models import Information

# Register your models here.


class InfomationAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Information.objects.count() > 0:
            return False
        return super().has_add_permission(request)


admin.site.register(Information, InfomationAdmin)
