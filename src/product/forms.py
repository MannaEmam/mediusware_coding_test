from django.forms import forms, ModelForm, TextInput, Textarea, CheckboxInput
from product.models import Variant, Product, ProductVariantPrice, ProductImage


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantPriceForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = '__all__'


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductCreationMultiForm(ModelForm):
    form_classes = {
        'product': ProductForm,
        'product_variant_price': ProductVariantPriceForm,
        'product_image': ProductImageForm,
    }

    def save(self, commit=True):
        objects = super(ProductCreationMultiForm, self).save(commit=False)

        if commit:
            product = objects['product']
            product.save()
            product_variant_price = objects['product_variant_price']
            product_variant_price.product = product
            product_variant_price.save()
            product_image = objects['product_image']
            product_image.product = product
            product_image.save()

        return objects
