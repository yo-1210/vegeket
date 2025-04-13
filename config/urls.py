"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base.views.item_view import IndexListView
from base.views.item_view import ItemDetailView,CategoryListView,TagListView
from base.views.cart_views import CartListView
from base.views.cart_views import AddCartView, remove_from_cart
from base.views.pay_view import PayWithStripe, PaySuccessView, PayCancelView
from base.views.account_views import Login, SignUpView, AccountUpdateView, ProfileUpdateView
from base.views.order_views import OrderIndexView, OrderDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Account
    path('login/', Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('account/', AccountUpdateView.as_view()),
    path('profile/', ProfileUpdateView.as_view()),

    # Pay
    path('pay/checkout/', PayWithStripe.as_view()),
    path('pay/success/', PaySuccessView.as_view()),
    path('pay/cancel/', PayCancelView.as_view()),

    # Order
    path('orders/<str:pk>/', OrderDetailView.as_view()),
    path('orders/', OrderIndexView.as_view()),

    # Cart
    path('cart/remove/<str:pk>/', remove_from_cart),
    path('cart/add/', AddCartView.as_view()),
    path('cart/', CartListView.as_view()),

    # Items
    path('items/<str:pk>/', ItemDetailView.as_view()),
    path('categories/<str:pk>/', CategoryListView.as_view()),
    path('tags/<str:pk>/', TagListView.as_view()),
 
    path('', IndexListView.as_view()),  # トップページ
]
