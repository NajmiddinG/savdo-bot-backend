# Generated by Django 4.2.1 on 2023-06-08 11:24

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('lan', models.CharField(default='uz', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Foydalanuvchi ',
                'verbose_name_plural': '1. Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Buyurtma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('location', models.TextField(max_length=1000)),
                ('tel', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Buyurtma ',
                'verbose_name_plural': '4. Buyurtmalar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255, null=True)),
                ('kelish_narx', models.FloatField(default=0)),
                ('sotish_narx', models.FloatField(default=0)),
                ('brend', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('shtrix', models.CharField(max_length=255, unique=True)),
                ('xarakteristika', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('xarakteristika_ru', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Mahsulot ',
                'verbose_name_plural': '2. Mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='Savat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('location', models.TextField(max_length=1000)),
                ('tel', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.botuser')),
            ],
            options={
                'verbose_name': 'Savat ',
                'verbose_name_plural': '3. Savatlar',
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('buyurtma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.buyurtma')),
            ],
            options={
                'verbose_name': 'Daromad ',
                'verbose_name_plural': '5. Daromadlar',
            },
        ),
        migrations.AddField(
            model_name='buyurtma',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.product'),
        ),
        migrations.AddField(
            model_name='buyurtma',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.botuser'),
        ),
    ]
