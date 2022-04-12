"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from customers.api.viewsets import CustomersViewSet
from products.api.viewsets import ProductsViewSet
from sales.api.viewsets import SalesViewSet, SalesItemsViewSet
from sellers.api.viewsets import SellersViewSet

router = DefaultRouter()
router.register(r'costumers', CustomersViewSet, basename="clientes")
router.register(r'products', ProductsViewSet, basename="produtos")
router.register(r'sales', SalesViewSet, basename="vendas")
router.register(r'sales_items', SalesItemsViewSet, basename="itens_vendas")
router.register(r'sellers', SellersViewSet, basename="vendedores")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
