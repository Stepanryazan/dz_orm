from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()
        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(version_current_sign=True)
            if active_versions:
                product.active_version = active_versions.last().version_name
                product.active_version_number = active_versions.last().version_number
            else:
                product.active_version = "-"
                product.active_version_number = "-"
        context_data['object_list'] = products
        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


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