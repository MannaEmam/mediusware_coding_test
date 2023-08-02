from django.core.paginator import Paginator
from django.views import generic
from product.models import Variant, Product, ProductVariant, ProductVariantPrice, ProductImage
from product.forms import ProductForm, ProductVariantPriceForm, ProductImageForm, ProductCreationMultiForm
from django.forms import inlineformset_factory, modelformset_factory


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
    pass

    # template_name = 'products/create.html'
    #
    def get_context_data(self, *args, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    # class CreateProductView(BaseProductView, generic.CreateView):
    #     template_name = 'products/create.html'
    #     success_url = '/product/list/'
    #     product_form = ProductForm
    #     product_variant_price_form = ProductVariantPriceForm
    #     product_image_form = ProductImageForm
    #
    #     def post(self, request):
    #         post_data = request.POST or None
    #         print(request.POST)
    #         print(request.FILES)
    #         product_form = self.product_form(post_data, prefix='product')
    #         product_variant_price_form = self.product_variant_price_form(post_data, prefix='product_variant_price')
    #         product_image_form = self.product_image_form(post_data, prefix='product_image')
    #
    #         context = self.get_context_data(product_form=product_form,
    #                                         product_variant_price_form=product_variant_price_form,
    #                                         product_image_form=product_image_form)
    #
    #         if product_form.is_valid():
    #             self.form_save(product_form)
    #         if product_variant_price_form.is_valid():
    #             self.form_save(product_variant_price_form)
    #         if product_image_form.is_valid():
    #             self.form_save(product_image_form)
    #
    #         return self.render_to_response(context)
    #
    #     def form_save(self, form):
    #         obj = form.save()
    #         messages.success(self.request, "{} saved successfully".format(obj))
    #         return obj
    #
    #     def get(self, request, *args, **kwargs):
    #         return self.post(request, *args, **kwargs)

    # form_classes = {
    #     'product_form': ProductForm,
    #     'product_variant_price_form': ProductVariantPriceForm,
    #     'product_image_form': ProductImageForm,
    # }
    # def forms_valid(self, forms):
    #     product_form = forms['product_form']
    #     product_variant_price_form = forms['product_variant_price_form']
    #     product_image_form = forms['product_image_form']
    #     product = product_form.save()
    #     product_variant_price_form.instance = product
    #     product_variant_price_form.save()
    #     product_image_form.instance = product
    #     product_image_form.save()

    # return super().forms_valid(forms)

    # def get_context_data(self, *args, **kwargs):
    #     print(kwargs)
    #     context = super(CreateProductView, self).get_context_data(**kwargs)
    #     variants = Variant.objects.filter(active=True).values('id', 'title')
    #     context['product'] = True
    #     context['variants'] = list(variants.all())
    #     return context

# class CreateProductView( generic.TemplateView):
# fields = ['title', 'sku', 'description']
# model = Product
# template_name = 'products/create.html'
# success_url = '/product/list'
# ProductFormSet = modelformset_factory(Product, fields=['title', 'sku', 'description'])
# ProductImageFormSet = inlineformset_factory(Product,ProductImage ,fields=['file_path'])
# ProductVariantPriceFormSet = inlineformset_factory(Product, ProductVariantPrice, fields=['product_variant_one', 'product_variant_two',
#                                                                                     'product_variant_three','price', 'stock'], extra=1)
#
# def get_context_data(self, **kwargs):
#
#     context = super().get_context_data(**kwargs)
#     ProductVariantPriceFormSet = inlineformset_factory(Product, ProductVariantPrice, fields=('product_variant_one', 'product_variant_two', 'product_variant_three',
#                                                                                              'price', 'stock'),extra=1)
#     print(context)
#     context['formset'] = ProductVariantPriceFormSet(self.request.POST or None)
#     return context

# def form_valid(self, form):
#     context = self.get_context_data()
#     formset = context['formset']
#     if formset.is_valid():
#         self.object = form.save()
#         formset.instance = self.object
#         formset.save()
#         return super().form_valid(form)
#     else:
#         return self.render_to_response(self.get_context_data(form=form))


# def post(self, request, *args, **kwargs):
#     print(request.POST)
#     print(args)
#     print(kwargs)
#     formset = self.ProductFormSet(request.POST)
#     if formset.is_valid():
#         product = formset.save()
#     else:
#         print("1", formset.error_messages)

# formset = self.ProductVariantPriceFormSet(request.POST, request.FILES, instance=product)
# if formset.is_valid():
#     formset.save()
# else:
#     print("2", formset.errors)
#
# formset = self.ProductImageFormSet(request.POST, request.FILES, instance=product)
# if formset.is_valid():
#     formset.save()
# else:
#     print("3", formset.errors)

# return self.render_to_response(self.get_context_data())
