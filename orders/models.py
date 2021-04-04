from django.db import models
from shop.models import Product
from gifting.models import ProductGifting, Variants
from django.urls import reverse
import  random
import string


class Customer(models.Model):

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    reffered_by = models.ForeignKey('self',on_delete=models.CASCADE, default=None, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, default=None, blank=True, null=True)
    referral_code = models.CharField(max_length=300, blank=True, null=True, unique=True)
    refer_count = models.IntegerField(default=0)
    first_ten_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('orders:order_create', args=[self.phone, self.email])


    def generate_referral_code(self):
        text = "#DOTCH.IN"
        text = text + ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(5)])
        print(text)
        return text



    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_code = self.generate_referral_code()
        return super(Customer,self).save(*args,**kwargs)

    class Meta:
        ordering = ('-created',)
        index_together = (('email','phone'),)



    def __str__(self):
        return "{} {} with email {} and phone {}".format(self.first_name,self.last_name,self.email, self.phone  )


class Review(models.Model):
    name = models.CharField(max_length=200, default=None, null=True)
    review = models.TextField(max_length=600, null=True)
    stars = models.IntegerField(default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "id"



class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None, null=True, related_name='ordered')
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    preferred_contact = models.CharField(max_length=100, null=True)
    referral_code = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)



    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    priceS = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    priceM = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    priceL = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    priceXL = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    priceXXL = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantityS = models.PositiveIntegerField(default=1, null=True)
    quantityM = models.PositiveIntegerField(default=1, null=True)
    quantityL = models.PositiveIntegerField(default=1, null=True)
    quantityXL = models.PositiveIntegerField(default=1, null=True)
    quantityXXL = models.PositiveIntegerField(default=1, null=True)


    def __str__(self):
        return '{}'.format(self.id)



class OrderItem_Gifts(models.Model):

    order = models.ForeignKey(Order, related_name='items_gifts', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductGifting, related_name='order_items_gifts', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, related_name='variants', on_delete=models.CASCADE, default=None, null=True)
    description = models.TextField(max_length=700, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image = models.ImageField(upload_to='User-Images/%Y/%m/%d', blank=True)
    expected_by = models.CharField(max_length=20, default=None, null=True)



    def __str__(self):
        return '{}'.format(self.id)



class OrderItem_bulk(models.Model):

    order = models.ForeignKey(Order, related_name='bulk', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items_bulk', on_delete=models.CASCADE, default=None, null=True)
    description = models.TextField(max_length=700, null=True, default=None)
    quantity = models.IntegerField(null=True)
    expected_by = models.CharField(max_length=20, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.id)


class OrderItem_stitching(models.Model):

    order = models.ForeignKey(Order, related_name='stitched', on_delete=models.CASCADE)
    description = models.TextField(max_length=700, null=True, default=None)
    service = models.CharField(max_length=25, default=None)
    expected_by = models.CharField(max_length=20, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.id)










