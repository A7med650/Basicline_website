from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, ReviewRating, ProductGallery, Wishlist, Compositions
from category.models import Category
from .forms import ReviewRatingForm
from django.db.models import Q
import json
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
from photos.models import Instagram, BaseInstagram, Banner
from category.context_processors import menu_links

# Create your views here.


def home(request):
    products = Product.objects.filter(is_available=True)

    list_product_variation = []
    for product in products:
        product_id = product.variation_set.values_list(
            'variation_category').count()
        if product_id >= 2:
            list_product_variation.append(product.id)
    products = products.filter(pk__in=list_product_variation)

    product_images = ProductGallery.objects.all().select_related('product')
    products_women = Product.objects.filter(
        is_available=True, is_man=False, pk__in=list_product_variation).select_related('category')
    base_instagram = BaseInstagram.objects.all().first()
    instagram_images = Instagram.objects.filter(
        instagram=base_instagram)
    banners = Banner.objects.filter(id=1).first()
    product_women_list = []
    for product in products_women:
        product_women_list.append(product.category.category_name)
        if len(set(product_women_list)) == 3:
            break
    products_man = Product.objects.filter(
        is_available=True, is_man=True, pk__in=list_product_variation).select_related('category')
    product_man_list = []
    for product in products_man:
        product_man_list.append(product.category.category_name)
        if len(set(product_man_list)) == 3:
            break
    context = {
        'products': products,
        'product_images': product_images,
        'products_women': products_women,
        'products_man': products_man,
        'category_women': sorted(list(set(product_women_list))),
        'category_man': sorted(list(set(product_man_list))),
        'instagram_images': instagram_images,
        'banners': banners,
    }
    return render(request, 'index.html', context)


def store(request, category_slug=None):
    categories = None
    products = None
    wishlist = Wishlist.objects.all().select_related("product")

    if category_slug != None:
        if category_slug not in set(menu_links(request)['categories_views']):
            raise Http404()
        categories = get_object_or_404(Category, slug=category_slug)

        products = Product.objects.filter(
            category=categories, is_available=True).order_by('id')
        list_product_variation = []
        for product in products:
            product_id = product.variation_set.values_list(
                'variation_category').count()
            if product_id >= 2:
                list_product_variation.append(product.id)
        products = products.filter(pk__in=list_product_variation)

        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
    else:
        products = Product.objects.filter(is_available=True).order_by('?')
        list_product_variation = []
        for product in products:
            product_id = product.variation_set.values_list(
                'variation_category').count()
            if product_id >= 2:
                list_product_variation.append(product.id)
        products = products.filter(pk__in=list_product_variation)
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
    context = {
        'products': paged_products,
        'categories': categories,
        'wishlist': wishlist,
    }
    return render(request, 'categories.html', context)


def product_detail(request, category_slug, product_slug):
    if category_slug not in set(menu_links(request)['categories_views']):
        raise Http404()
    single_product = get_object_or_404(
        Product.objects.select_related('category'), category__slug=category_slug, slug=product_slug)
    related_products = Product.objects.filter(category__slug=category_slug)

    list_product_variation = []
    for product in related_products:
        product_id = product.variation_set.values_list(
            'variation_category').count()
        if product_id >= 2:
            list_product_variation.append(product.id)
    related_products = related_products.filter(pk__in=list_product_variation)

    compositions = Compositions.objects.filter(product=single_product)

    product_gallery = ProductGallery.objects.filter(product=single_product)
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)
    colors = single_product.variation_set.colors
    sizes = single_product.variation_set.sizes
    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
        'reviews': reviews,
        'colors': colors,
        'sizes': sizes,
        'related_products': related_products,
        'compositions':compositions,
    }
    return render(request, 'product-details.html', context)


def women(request):
    products_women = Product.objects.filter(
        is_available=True, is_man=False).order_by('?')

    list_product_variation = []
    for product in products_women:
        product_id = product.variation_set.values_list(
            'variation_category').count()
        if product_id >= 2:
            list_product_variation.append(product.id)
    products_women = products_women.filter(pk__in=list_product_variation)

    paginator = Paginator(products_women, 3)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    context = {
        'products': paged_products,
        'categories': 'Women',
    }
    return render(request, 'categories.html', context)


def man(request):
    products_man = Product.objects.filter(
        is_available=True, is_man=True).order_by('?')

    list_product_variation = []
    for product in products_man:
        product_id = product.variation_set.values_list(
            'variation_category').count()
        if product_id >= 2:
            list_product_variation.append(product.id)
    products_man = products_man.filter(pk__in=list_product_variation)

    paginator = Paginator(products_man, 3)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    context = {
        'products': paged_products,
        'categories': 'Man',
    }
    return render(request, 'categories.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)


def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        products = Product.objects.filter(
            Q(description__icontains=query) | Q(product_name__icontains=query))
        list_product_variation = []
        for product in products:
            product_id = product.variation_set.values_list(
                'variation_category').count()
            if product_id >= 2:
                list_product_variation.append(product.id)
        products = products.filter(pk__in=list_product_variation)
        context = {
            'products': products,
        }
        return render(request, 'categories.html', context)
    return redirect('home')


def search_auto(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        query = request.GET.get('term', '')
        products = Product.objects.filter(
            Q(description__icontains=query) | Q(product_name__icontains=query))
        list_product_variation = []
        for product in products:
            product_id = product.variation_set.values_list(
                'variation_category').count()
            if product_id >= 2:
                list_product_variation.append(product.id)
        products = products.filter(pk__in=list_product_variation)
        results = []
        for product in products:
            product_json = {}
            product_json = product.product_name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_quick_view(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product_pk': product.id,
    }
    return JsonResponse(context)


def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    try:
        wishlist = Wishlist.objects.get(product=product, user=user)
        wishlist.delete()
    except:
        wishlist = Wishlist.objects.create(product=product, user=user)
    context = {
        'product_pk': product.id,
    }
    return JsonResponse(context)


@login_required(login_url='register_and_login')
def wishlist_page(request):
    wishlist = Wishlist.objects.filter(
        user=request.user).select_related("product")
    context = {
        "wishlist": wishlist,
    }
    return render(request, "wishlist.html", context)


@login_required(login_url='register_and_login')
def remove_product_wishlist(request, pk):
    wishlist = Wishlist.objects.get(id=pk)
    wishlist_id = wishlist.id
    context = {
        'wishlist_id': wishlist_id,
    }
    wishlist.delete()
    return JsonResponse(context)
