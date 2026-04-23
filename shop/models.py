from django.db import models
from cloudinary.models import CloudinaryField

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    category_name = models.CharField(max_length=200, default='')
    sub_category_name = models.CharField(max_length=200 ,default='')
    price = models.IntegerField(default=0)
    product_description = models.CharField(max_length=300)
    pub_date = models.DateField( )
    image = CloudinaryField('image', blank=True, null=True)
    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default='')
    phone = models.CharField(max_length=70 ,default='')
    message = models.CharField(max_length=500,default='')


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.JSONField(default=list)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=20)
    total_amount = models.IntegerField(default=0)
    order_status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="updates")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[:50] + "..."