from django.db import models

# Create your models here.
# this is the model for the products table.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True) # auto-incrementing primary key field.
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True) # sku means stock keeping unit.
    price = models.FloatField() # the price can also be written as models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/', blank=True, null=True) # this is used to upload images to the database.

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ''

# this is the model for the users table.
class User(models.Model):
    user_id = models.AutoField(primary_key=True) # auto-incrementing primary key field.
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name