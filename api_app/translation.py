from modeltranslation.translator import translator, TranslationOptions
from .models import Product

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'xarakteristika')

translator.register(Product, ProductTranslationOptions)