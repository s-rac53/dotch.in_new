from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Category


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


        category = fields.ObjectField(
            properties = {
                'name':fields.TextField(),
                'slug': fields.TextField()
            }
        )


        class Django:
            model = Product
            fields = ['name','slug', 'description',]


