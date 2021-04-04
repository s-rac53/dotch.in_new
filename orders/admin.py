from django.contrib import admin
from .models import Order, OrderItem, Customer, OrderItem_Gifts, OrderItem_bulk, Review, OrderItem_stitching

class OrderItemStitchingInline(admin.TabularInline):
    model = OrderItem_bulk

class OrderItemBulkInline(admin.TabularInline):
    model = OrderItem_stitching


class OrderItemGiftsInline(admin.TabularInline):
    model = OrderItem_Gifts
    raw_id_fields = ['product','variant']


class OrderItemInline(admin.TabularInline):
     model = OrderItem
     raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     list_display = ['id', 'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
     list_filter = ['paid', 'created', 'updated','customer']
     inlines = [OrderItemInline, OrderItemGiftsInline, OrderItemBulkInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ['id','first_name','last_name','email','phone','referral_code','created','order_numbers', ]
    list_filter = ['id','first_name','last_name','email','phone','referral_code','created', ]


    def order_numbers(self,obj):
        return obj.ordered.name


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ['name','review','created']
    list_filter = ['name','created']
















