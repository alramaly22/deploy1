from django.contrib import admin
from .models import Category, Customer, Product, ProductImage, Order, Profile, FeaturedImage
from django.contrib.auth.models import User

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # عدد الحقول الافتراضي لإضافة الصور

# إدارة المنتج
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_sale']
    search_fields = ['name']
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

# تسجيل الفئات
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)

# إدارة العميل (Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'user')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('user',)

admin.site.register(Customer, CustomerAdmin)

# إدارة الصور المميزة
class FeaturedImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes_count')  # عرض الحقول المطلوبة في لوحة الإدارة
    search_fields = ('title',)  # إضافة مربع البحث
    filter_horizontal = ('liked_by',)  # لإظهار الحقل بشكل متعدد

admin.site.register(FeaturedImage, FeaturedImageAdmin)

# تخصيص المستخدم وربط الملف الشخصي
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fieldsets = [
        ("User Info", {"fields": ["username", "first_name", "last_name", "email"]}),
    ]
    inlines = [ProfileInline]

# إعادة تسجيل نموذج المستخدم مع التخصيص
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
