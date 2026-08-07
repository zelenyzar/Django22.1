from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from django.conf import settings
from .views import products_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

