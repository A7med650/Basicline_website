from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('view-order/<order_number>/',
         views.view_order_products, name='view_order'),
]
