import pandas as pd
from PIL import Image
from io import BytesIO
import datetime
from django.conf import settings
import os
import openpyxl
from openpyxl_image_loader import SheetImageLoader

from .models import Product

def import_data(file_path):
    df = pd.read_excel(file_path, header=0)
    pxl_doc = openpyxl.load_workbook(file_path)
    sheet = pxl_doc.active
    image_loader = SheetImageLoader(sheet)

    for index, row in df.iterrows():
        try:
            product = Product()
            product.name = row[0]
            product.kelish_narx = row[1]
            product.sotish_narx = row[2]
            product.brend = row[3]
            product.shtrix = row[4]
            try:
                image = image_loader.get(row[5])
                if image:
                    image.show()
                    current_time = datetime.datetime.now()
                    filename = f"image_{current_time.strftime('%Y%m%d%H%M%S')}.jpg"
                    image_path = os.path.join(settings.MEDIA_ROOT, 'products', filename)
                    image.save(image_path)
                    product.image = os.path.join('products', filename)
            except: pass
            product.save()
        except: pass