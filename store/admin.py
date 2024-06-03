from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery, Wishlist, Compositions

# Register your models here.


class ProductGalleryInline(admin.StackedInline):
    model = ProductGallery
    extra = 0
    min_num = 4
    max_num = 4
    can_delete = False


class VariationInline(admin.StackedInline):
    model = Variation
    extra = 0
    min_num = 2


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category',
                    'modified_date', 'is_man', 'is_available']
    # prepopulated_fields = {'slug': ('product_name', )}
    inlines = [ProductGalleryInline, VariationInline]
    # exclude = ('slug',)
    readonly_fields = ['slug', ]


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size']
    list_filter = ['product', 'color', 'size', ]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']


class CompositionAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']


admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)

# admin.site.register(Variation, VariationAdmin)

admin.site.register(ReviewRating)
admin.site.register(Compositions, CompositionAdmin)
