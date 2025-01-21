from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FeaturedImage


def toggle_like(request, image_id):
    image = get_object_or_404(FeaturedImage, id=image_id)

    if request.user.is_authenticated:
        # إذا كان المستخدم مسجلاً
        if request.user in image.liked_by.all():
            image.liked_by.remove(request.user)
            image.likes_count -= 1
            liked = False
        else:
            image.liked_by.add(request.user)
            image.likes_count += 1
            liked = True
    else:
        # إذا كان المستخدم غير مسجل
        liked_images = request.session.get('liked_images', [])

        if image_id in liked_images:
            liked_images.remove(image_id)
            image.likes_count -= 1
            liked = False
        else:
            liked_images.append(image_id)
            image.likes_count += 1
            liked = True

        # تحديث الجلسة
        request.session['liked_images'] = liked_images
        request.session.modified = True

    # حفظ التغيرات في قاعدة البيانات
    image.save()

    return JsonResponse({'likes_count': image.likes_count, 'liked': liked})


@login_required
def update_info(request):
    # الحصول على الملف الشخصي للمستخدم
    current_user = Profile.objects.get(user__id=request.user.id)

    # إذا تم إرسال الفورم
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=current_user)
        if form.is_valid():
            print("Form data:", form.cleaned_data)  # طباعة البيانات المرسلة
            form.save()
            messages.success(request, "Your information has been updated!")
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # طباعة الأخطاء إذا كانت هناك
    else:
        form = UserInfoForm(instance=current_user)

    return render(request, 'update_info.html', {'form': form})
@login_required
def update_password(request):
    current_user = request.user
    # Did they fill out the form
    if request.method == 'POST':
        form = ChangePasswordForm(current_user, request.POST)
        # Is the form valid
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Has Been Updated...")
            login(request, current_user)
            return redirect('update_user')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('update_password')
    else:
        form = ChangePasswordForm(current_user)
        return render(request, "update_password.html", {'form': form})


@login_required
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    if user_form.is_valid():
        user_form.save()
        login(request, current_user)
        messages.success(request, "User Has Been Updated!!!")
        return redirect('home')
    return render(request, "update_user.html", {'user_form': user_form})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})


def category(request, foo):
    foo = foo.replace('_', '')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.success(request, "That Category Doesn't Exist.......")
        return redirect('home')


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # استرجاع الصور المرتبطة بالمنتج
    product_images = product.images.all()
    return render(request, 'product.html', {'product': product, 'product_images': product_images})


def home(request):
    products = Product.objects.all()
    featured_images = FeaturedImage.objects.all()
    liked_images = request.user.liked_images.values_list('id', flat=True) if request.user.is_authenticated else []

    return render(request, 'home.html', {
        'products': products,
        'featured_images': featured_images,
        'liked_images': liked_images,
    })


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out ....Thanks For Stopping By.........")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log In User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your User Info Below")
            return redirect('update_info')
        else:
            # Debugging: Display form errors
            messages.error(request, "There was an error in your form: " + str(form.errors))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def coming_soon(request):
    return render(request, 'comingsoon.html', {})