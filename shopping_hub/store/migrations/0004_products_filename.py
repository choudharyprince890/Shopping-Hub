# Generated by Django 4.2.2 on 2023-06-30 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='filename',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]