from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('store/category/women/', views.women, name='women'),
    path('store/category/man/', views.man, name='man'),
    path('store/category/<slug:category_slug>/',
         views.store, name='products_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
    path('store/search/', views.search, name='search'),
    path('store/search-auto/', views.search_auto, name='search_auto'),
    path('store/submit-review/<int:product_id>/',
         views.submit_review, name='submit_review'),
    path('product-quick-view/<id>', views.product_quick_view,
         name='product_quick_view'),
    path('add-to-wishlist/<id>', views.add_to_wishlist,
         name='add_to_wishlist'),
    path("wishlist/", views.wishlist_page, name="wishlist"),
    path("remove-wishlist-item/<pk>/", views.remove_product_wishlist,
         name="remove_wishlist_item"),
]
