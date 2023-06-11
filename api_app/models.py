from django.db import models
from ckeditor.fields import RichTextField
from modeltranslation import settings as mt_settings


class BotUser(models.Model):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    lan = models.CharField(max_length=10, default='uz')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Foydalanuvchi '
        verbose_name_plural = '1. Foydalanuvchilar'


class Product(models.Model):
    name = models.CharField(max_length=255)
    kelish_narx = models.FloatField(default=0)
    sotish_narx = models.FloatField(default=0)
    brend = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    shtrix = models.CharField(max_length=255, unique=True)
    xarakteristika = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Mahsulot '
        verbose_name_plural = '2. Mahsulotlar'


class Savat(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    location = models.TextField(max_length=1000)
    tel = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date.strftime("%Y-%m-%d %H:%M:%S"))
    
    class Meta:
        verbose_name = 'Savat '
        verbose_name_plural = '3. Savatlar'


class Buyurtma(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    location = models.TextField(max_length=1000)
    tel = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.date.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name = 'Buyurtma '
        verbose_name_plural = '4. Buyurtmalar'


class Income(models.Model):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    full_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name = 'Daromad '
        verbose_name_plural = '5. Daromadlar'

if mt_settings.AUTO_POPULATE:
    mt_settings.AUTO_POPULATE = False