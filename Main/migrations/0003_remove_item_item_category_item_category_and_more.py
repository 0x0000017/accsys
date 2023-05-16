# Generated by Django 4.1.3 on 2023-05-16 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='item_category',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
