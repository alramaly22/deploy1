from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal

def cart_summary(request):
    # الحصول على عربة التسوق
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    # رسوم التوصيل ثابتة ب 60 جنيه
    delivery_fee = Decimal('60.00')
    total_with_delivery = totals + delivery_fee

    return render(request, "cart_summary.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "total_with_delivery": total_with_delivery,
        "delivery_fee": delivery_fee
    })
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = request.POST.get('product_size')  # الحصول على المقاس
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty, size=product_size)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = request.POST.get('product_size')  # الحصول على المقاس
        cart.update(product=product_id, quantity=product_qty, size=product_size)
        response = JsonResponse({'qty': product_qty, 'size': product_size})
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response