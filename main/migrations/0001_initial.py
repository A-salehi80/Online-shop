# Generated by Django 4.2.7 on 2024-02-21 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('is_payed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('image', models.FileField(upload_to='img/category')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('brand', models.CharField(blank=True, max_length=128, null=True)),
                ('model', models.CharField(blank=True, max_length=128, null=True)),
                ('ID_NO', models.CharField(blank=True, max_length=225, null=True, unique=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='img/items')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('tags', models.ManyToManyField(to='main.tag')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='main.CartItem', to='main.item'),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('subtitle', models.CharField(blank=True, max_length=225, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='img/blog/')),
                ('content', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('ID_NO', models.CharField(blank=True, max_length=225, null=True, unique=True)),
                ('tags', models.ManyToManyField(to='main.tag')),
            ],
        ),
    ]
