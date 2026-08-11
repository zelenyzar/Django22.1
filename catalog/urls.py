from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from .views import ProductListView, ProductDetailView
from django.conf import settings
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)