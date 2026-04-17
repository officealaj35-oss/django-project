from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path("" , views.index, name='shopname'),
    path("about/" , views.about, name='aboutUs'),
    path("contact/" , views.contact, name='contactUs'),
    path("tracker/", views.tracker, name="tracker"),
    path("search/" , views.search , name='search'),
    path("product/<int:id>/", views.product_view, name='product_view'),
    path("checkout/" , views.checkout, name='checkout'),
    path("checkout-success/", views.checkout_success, name="checkout_success"),

    # 🔥 Login system routes (NEW)
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-admin/', views.create_admin)
]

