# Generated by Django 3.1.7 on 2021-03-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_review_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.IntegerField(default=0, null=True),
        ),
    ]