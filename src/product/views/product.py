from django.core.paginator import Paginator
from django.views import generic
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from product.forms import ProductForm
from django.db.models import Q


class BaseProductView(generic.View):
    form_class = ProductForm
    model = Product
    template_name = 'products/create.html'
    success_url = '/product/list'


class ProductView(BaseProductView, generic.ListView):
    template_name = 'products/list.html'
    paginate_by = 2

    def get_queryset(self):
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        queryset = Product.objects.all()

        if title:
            queryset = queryset.filter(title__icontains=title)

        if variant:
            queryset = queryset.filter(productvariant__variant_title__icontains=variant)

        if price_from and price_to:
            queryset = queryset.filter(productvariantprice__price__range=(price_from, price_to))

        if date:
            queryset = queryset.filter(productvariantprice__created_at__date=date)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        context['product_list'] = paginator.get_page(page_number)
        context['variants'] = Variant.objects.all()
        return context


class CreateProductView(BaseProductView, generic.CreateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

