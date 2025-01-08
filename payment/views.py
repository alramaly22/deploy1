from django.shortcuts import render , redirect
from cart.cart import Cart
from payment.forms import ShippingForm , PaymentForm
from payment.models import ShippingAddress , Order ,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product , Profile
import datetime
# Create your views here.
def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')
def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')
from django.shortcuts import redirect
from django.contrib import messages

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        # استخراج بيانات الشحن
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"

        # حساب عدد المنتجات في السلة
        total_items = sum(quantities().values())

        # تحديد رسوم التوصيل (50 جنيه) إذا كان عدد المنتجات أقل من 3
        delivery_fee = 50 if total_items < 3 else 0

        # حساب الإجمالي الكلي مع رسوم التوصيل
        amount_paid = totals + delivery_fee

        if request.user.is_authenticated:
            # إذا كان المستخدم مسجل دخول
            user = request.user
            create_order = Order(
                user=user, 
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,  # إجمالي الطلب مع رسوم التوصيل
            )
            create_order.save()

            order_id = create_order.pk
            
            # إضافة العناصر إلى الطلب
            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id, 
                            product_id=product_id, 
                            user=user, 
                            quantity=value, 
                            price=price
                        )
                        create_order_item.save()

            # مسح السلة بعد تأكيد الطلب
            for key in list(request.session.keys()):  
                if key == "session_key":
                    del request.session[key]

            # عرض رسالة تأكيد مع رسوم التوصيل
            messages.success(request, f"Order Placed! Delivery Fee: {delivery_fee} EGP.") 
            return redirect('home')
        
        else:
            # إذا لم يكن المستخدم مسجل دخول
            messages.error(request, "You need to be logged in to place an order!")
            return redirect('login')  # أو redirect إلى صفحة التسجيل إذا كنت ترغب في ذلك
    else:
        messages.error(request, "Access Denied")
        return redirect('home')


		
def billing_info(request):
    if request.method == 'POST':
        # حفظ بيانات الشحن في الجلسة
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # التحقق من تسجيل الدخول
        if request.user.is_authenticated:
            cart = Cart(request)
            cart_products = cart.get_prods
            quantities = cart.get_quants()
            totals = cart.cart_total()
            
            # حساب عدد المنتجات الإجمالي
            total_items = sum(quantities.values())
            
            # تحديد رسوم التوصيل (50 جنيه) إذا كان عدد المنتجات أقل من 3
            delivery_fee = 50 if total_items < 3 else 0
            
            # حساب الإجمالي النهائي
            total_with_delivery = totals + delivery_fee
            
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,  # الإجمالي بدون التوصيل
                "total_with_delivery": total_with_delivery,  # الإجمالي مع التوصيل
                "delivery_fee": delivery_fee,  # رسوم التوصيل (50 أو 0)
                "shipping_info": my_shipping
            })
        else:
            messages.error(request, "You need to be logged in to proceed.")
            return redirect('login')
    else:
        messages.error(request, "Access Denied.")
        return redirect('home')



def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    # حساب عدد المنتجات الإجمالي
    total_items = sum(quantities.values())  # Calculate total quantity of products in cart
    
    # تحديد رسوم التوصيل (50 جنيه) إذا كان عدد المنتجات أقل من 3
    delivery_fee = 50 if total_items < 3 else 0
    
    # حساب المجموع النهائي مع رسوم التوصيل
    total_with_delivery = totals + delivery_fee

    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,  # المجموع بدون التوصيل
        "total_with_delivery": total_with_delivery,  # المجموع مع التوصيل
        "delivery_fee": delivery_fee,  # رسوم التوصيل (إما 50 أو 0)
        "shipping_form": shipping_form
    })

	

def payment_success(request):
	return render(request, "payment/payment_success.html", {})

