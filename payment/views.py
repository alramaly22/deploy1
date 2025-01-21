from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import datetime
from decimal import Decimal
from store.models import Profile  # استيراد Profile من تطبيق store
from store.forms import UserInfoForm  # استيراد UserInfoForm من تطبيق store

@login_required
def payment_success(request):
    """
    عرض صفحة نجاح الدفع.
    """
    return render(request, 'payment/payment_success.html', {})


@login_required
def checkout(request):
    """
    عرض صفحة الدفع مع تفاصيل العربة ورسوم التوصيل.
    """
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    # رسوم التوصيل ثابتة ب 60 جنيه
    delivery_fee = Decimal('60.00')
    total_with_delivery = totals + delivery_fee

    if request.user.is_authenticated:
        # الحصول على بيانات المستخدم من Profile
        shipping_user = Profile.objects.get(user__id=request.user.id)
        
        # إذا تم إرسال الفورم (تحديث البيانات)
        if request.method == 'POST':
            shipping_form = UserInfoForm(request.POST, instance=shipping_user)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, "Your shipping information has been updated!")
                return redirect('checkout')
        else:
            # تعبئة الفورم بالبيانات الحالية من Profile
            shipping_form = UserInfoForm(instance=shipping_user)
    else:
        messages.error(request, "You need to be logged in to proceed to checkout.")
        return redirect('login')

    return render(request, 'payment/checkout.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "total_with_delivery": total_with_delivery,
        "delivery_fee": delivery_fee,
        "shipping_form": shipping_form
    })


@login_required
def billing_info(request):
    """
    عرض صفحة معلومات الفوترة مع تفاصيل الشحن.
    """
    if request.method == 'POST':
        my_shipping = {
            'full_name': request.POST.get('shipping_full_name'),
            'email': request.POST.get('shipping_email'),
            'address': request.POST.get('shipping_address1'),
            'city': request.POST.get('shipping_city'),
            'state': request.POST.get('shipping_state'),
            'country': request.POST.get('shipping_country'),
        }
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            cart = Cart(request)
            cart_products = cart.get_prods()
            quantities = cart.get_quants()
            totals = cart.cart_total()

            # رسوم التوصيل ثابتة ب 60 جنيه
            delivery_fee = Decimal('60.00')
            total_with_delivery = totals + delivery_fee

            return render(request, 'payment/billing_info.html', {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "total_with_delivery": total_with_delivery,
                "delivery_fee": delivery_fee,
                "shipping_info": my_shipping  # تمرير البيانات إلى القالب
            })
        else:
            messages.error(request, "You need to be logged in to proceed.")
            return redirect('login')
    else:
        messages.error(request, "Access Denied.")
        return redirect('home')


@login_required
def process_order(request):
    """
    معالجة الطلب وإنشاء سجل الطلب في قاعدة البيانات.
    """
    if request.method == 'POST':
        my_shipping = request.session.get('my_shipping', {})
        
        # تحقق من وجود المفاتيح المطلوبة
        required_keys = ['full_name', 'email', 'address', 'city', 'state', 'country']
        if not all(key in my_shipping for key in required_keys):
            messages.error(request, "Shipping information is incomplete or missing.")
            return redirect('checkout')
        
        full_name = my_shipping['full_name']
        email = my_shipping['email']
        shipping_address = f"{my_shipping['address']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['country']}"

        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # رسوم التوصيل ثابتة ب 60 جنيه
        delivery_fee = Decimal('60.00')
        amount_paid = totals + delivery_fee

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            order_id = create_order.pk

            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price
                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value['quantity'] if isinstance(value, dict) else value,
                            price=price,
                            size=value['size'] if isinstance(value, dict) else None
                        )
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, f"Order Placed! Delivery Fee: {delivery_fee} EGP.")
            return redirect('home')

        else:
            messages.error(request, "You need to be logged in to place an order!")
            return redirect('login')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')


@login_required
def shipped_dash(request):
    """
    عرض لوحة التحكم للطلبات المشحونة (للمشرفين فقط).
    """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')


@login_required
def not_shipped_dash(request):
    """
    عرض لوحة التحكم للطلبات غير المشحونة (للمشرفين فقط).
    """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')


@login_required
def orders(request, pk):
    """
    عرض تفاصيل طلب معين (للمشرفين فقط).
    """
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')