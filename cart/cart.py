from decimal import Decimal
from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity, size=None):  # جعل size اختياري
        product_id = str(product)
        product_qty = quantity if isinstance(quantity, int) else quantity['quantity']  # استخراج الكمية من القاموس
        product_size = str(size) if size else 'One Size'  # قيمة افتراضية إذا لم يتم توفير size

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'quantity': int(product_qty), 'size': product_size}

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity, size):
        product_id = str(product.id)
        product_qty = str(quantity)
        product_size = str(size)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'quantity': int(product_qty), 'size': product_size}

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = Decimal('0.00')

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    quantity = value['quantity'] if isinstance(value, dict) else value
                    if product.is_sale:
                        total += Decimal(str(product.sale_price)) * Decimal(str(quantity))
                    else:
                        total += Decimal(str(product.price)) * Decimal(str(quantity))
        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return {product: self.cart[str(product.id)] for product in products}

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity, size):
        product_id = str(product)
        product_qty = int(quantity)
        product_size = str(size)
        ourcart = self.cart

        if product_id in ourcart:
            ourcart[product_id]['quantity'] = product_qty  # تحديث الكمية
            ourcart[product_id]['size'] = product_size  # تحديث المقاس
            self.session.modified = True

            if self.request.user.is_authenticated:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))