from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# الملف الشخصي للمستخدم
# في store/models.py

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)  # تأكد من وجود هذا الحقل
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username
# إنشاء ملف شخصي تلقائيًا عند إنشاء مستخدم جديد
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)

# الفئات
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

# العملاء
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# المنتجات
class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=700, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/', null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    sizes = models.CharField(max_length=100, blank=True, null=True)  # تأكد من وجود هذا الحقل
    def __str__(self):
        return self.name

# الصور المرتبطة بالمنتجات
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

# الطلبات
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.customer.first_name} - {self.product.name}"

# الصور المميزة
class FeaturedImage(models.Model):
    image = models.ImageField(upload_to='featured_images/')
    title = models.CharField(max_length=255, blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_images', blank=True)

    def __str__(self):
        return self.title or "Featured Image"