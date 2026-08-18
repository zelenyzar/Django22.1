from itertools import product

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Product
from catalog.forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_unpublish_product"] = user.has_perm("catalog.can_unpublish_product")
        context["can_delete_product"] = user.has_perm("catalog.delete_product")
        context["can_change_product"] = user.has_perm("catalog.change_product")

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_unpublish_product"] = user.has_perm("catalog.can_unpublish_product")
        context["can_delete_product"] = user.has_perm("catalog.delete_product")
        context["can_change_product"] = user.has_perm("catalog.change_product")
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")
    permission_required = "catalog.change_product"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != self.request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Вы не можете редактировать чужой продукт")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")
    permission_required = 'catalog.delete_product'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        can_delete = (
                product.owner == request.user
                or request.user.has_perm("catalog.delete_product")
        )
        if not can_delete:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("У вас нет прав на удаление этого продукта")
        return super().dispatch(request, *args, **kwargs)


@method_decorator(permission_required("catalog.can_unpublish_product", raise_exception=True), name="dispatch")
class UnpublishProductView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])
        return redirect("catalog:products_list")


