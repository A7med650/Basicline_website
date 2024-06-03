from django.urls import path
from . import views

urlpatterns = [
    path('register-and-login/', views.register_and_login,
         name='register_and_login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/', views.forgot_password, name="forgotpassword"),
    path('reset-password-validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('change-password/', views.change_password, name="change_password"),
]
