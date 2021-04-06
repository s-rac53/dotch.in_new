from django.db import models
from django.urls import reverse


class ProductGifting(models.Model):

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.FileField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('gifting:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('name',)

    index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Variants(models.Model):
    product = models.ForeignKey(ProductGifting, related_name='variants', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.FileField(upload_to='products/variations/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('gifting:product_detail', args=[self.id, self.slug])
    class Meta:
        ordering = ('name',)
    index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(ProductGifting,related_name='images', on_delete=models.CASCADE)
    images = models.FileField(upload_to='products/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)




