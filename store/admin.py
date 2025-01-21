from django.contrib import admin
from .models import Category, Customer, Product, ProductImage, Order, Profile, FeaturedImage
from django.contrib.auth.models import User

# إدارة صور المنتج
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # عدد الحقول الافتراضي لإضافة الصور

# إدارة المنتج
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_sale', 'sizes']
    search_fields = ['name']
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

# تسجيل الفئات
admin.site.register(Category)
admin.site.register(Order)

# إدارة الملف الشخصي (Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'email', 'address', 'city', 'state', 'country', 'old_cart')
    search_fields = ('user__username', 'full_name', 'email', 'phone')
    list_filter = ('user',)

admin.site.register(Profile, ProfileAdmin)

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
    fields = ('full_name', 'phone', 'email', 'address', 'city', 'state', 'country', 'old_cart')  # الحقول الجديدة
    extra = 1  # عدد الحقول الافتراضي لإضافة الملف الشخصي

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name')  # الحقول المعروضة في قائمة المستخدمين
    search_fields = ('username', 'email', 'first_name', 'last_name')  # البحث حسب هذه الحقول
    inlines = [ProfileInline]  # إضافة ProfileInline

# إعادة تسجيل نموذج المستخدم مع التخصيص
admin.site.unregister(User)
admin.site.register(User, UserAdmin)