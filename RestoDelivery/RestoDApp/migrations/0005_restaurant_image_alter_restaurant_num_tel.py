# Generated by Django 4.0.4 on 2022-05-22 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestoDApp', '0004_alter_categorie_description_alter_restaurant_menu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, upload_to='resto_images/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='num_tel',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
