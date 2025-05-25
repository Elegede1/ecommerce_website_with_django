from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True) # auto-incrementing primary key field.
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True) # sku means stock keeping unit.
    price = models.FloatField() # the price can also be written as models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
