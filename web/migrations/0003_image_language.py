# Generated by Django 2.2.3 on 2019-07-16 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20190716_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='language',
            field=models.CharField(default='pol', max_length=5),
        ),
    ]
