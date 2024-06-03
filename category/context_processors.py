from .models import Category
from store.models import Product


def menu_links(request):
    links = Category.objects.all()
    products = Product.objects.select_related('category')

    list_product_variation = []
    for product in products:
        product_id = product.variation_set.values_list(
            'variation_category').count()
        if product_id >= 2:
            list_product_variation.append(product.id)
    products = products.filter(pk__in=list_product_variation)

    categories = []
    for product in products:
        categories.append(product.category.slug)
    links = links.filter(slug__in=categories)
    return dict(links=links, categories_views=categories)
