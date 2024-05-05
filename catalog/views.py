from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f"Message from {name} (Tel: {phone}): {message}")
        return render(request, self.template_name)