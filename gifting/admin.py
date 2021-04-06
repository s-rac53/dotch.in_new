from django.contrib import admin
from gifting.models import ProductGifting, ProductImage, Variants


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(ProductGifting)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageAdmin]

    class Meta:
        model = ProductGifting


@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'price', 'available', 'created', 'updated']
    list_filter = ['product', 'name', 'price', 'available', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass