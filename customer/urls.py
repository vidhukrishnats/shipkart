from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.allProducts, name="allproducts"),
    path('product/<slug:slug>/', views.productDetail, name="product"),
    path('category/<slug:category_slug>/', views.categoryList, name="category_list"),
    path('search/', views.search, name="search"),
    path('login/', views.loginPage, name="login"),
    path('custom_logout/', views.customLogout, name="custom_logout"),
    path('register/', views.registerUser, name="register"),
    path('activate/<uidb64>/<token>', views.activateUser, name="activate"),
    path('profile/<username>/', views.profile, name="profile"),
    path('forgot_password/', views.forgotPassword, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>/', views.resetPasswordValidate, name="reset_password_validate"),
    path('reset_password/', views.resetPassword, name="reset_password"),
]

