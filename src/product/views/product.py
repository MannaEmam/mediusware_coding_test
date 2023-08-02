from django.core.paginator import Paginator
from django.views import generic
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from product.forms import ProductForm
from django.views.generic import ListView, CreateView, UpdateView


class BaseProductView(generic.View):
    form_class = ProductForm
    model = Product
    template_name = 'products/create.html'
    success_url = '/product/list'


class ProductView(BaseProductView, generic.ListView):
    template_name = 'products/list.html'
    paginate_by = 2

    def get_queryset(self):
        filter_string = {}
        for key in self.request.GET:
            if key != 'page' and self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Product.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request.GET.get('title__icontains', '')
        paginator = Paginator(context['object_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        context['product_list'] = paginator.get_page(page_number)
        return context


class CreateProductView(BaseProductView, generic.CreateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

