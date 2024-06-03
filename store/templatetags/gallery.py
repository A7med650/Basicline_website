from django import template
from store.models import Product, ProductGallery, Wishlist

register = template.Library()


@register.simple_tag()
def images(product, index, *args, **kwargs):
    product_gallery = ProductGallery.objects.filter(
        product=product)
    if product_gallery.count() == 0:
        return None
    if product_gallery[index].image.url is None:
        return None
    return product_gallery[index].image.url


@register.simple_tag()
def color(product, *args, **kwargs):
    colors = product.variation_set.colors
    return colors


@register.simple_tag()
def size(product, *args, **kwargs):
    sizes = product.variation_set.sizes
    return sizes


@register.simple_tag()
def check_product_in_wishlist(product, *args, **kwargs):
    return Wishlist.objects.filter(product_id=product).exists()
