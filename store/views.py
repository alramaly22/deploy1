from django.shortcuts import render, redirect
from .models import Product, Category , Profile
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm , UpdateUserForm ,ChangePasswordForm , UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
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
def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)

        # Try to get the user's shipping info, or create a new instance
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)

        # Get original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST' and (form.is_valid() and shipping_form.is_valid()):
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()

            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')

        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
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
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm (request.POST or None , instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request,"User Has Been Update!!!")
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"You Must Be Logged In To Access That Page!!")
        return redirect('home')

    # return render(request,'update_user.html',{})
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})

def category (request , foo):
    foo = foo.replace ('_' , '')
    try:
        category = Category.objects.get(name= foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products , 'category':category})
    except:
        messages.success(request,("That Category Doesn't Exist......."))
        return redirect('home') 

def product(request, pk):
    product = Product.objects.get(id=pk)
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

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out ....Thanks For Stopping By........."))
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

