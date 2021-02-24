from django.contrib import admin
from shop.models import Category, Product, ProductImage, ProductSize


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductImageAdmin(admin.StackedInline):
    model = ProductSize


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
      'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id',)
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    pass


