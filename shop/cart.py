from decimal import Decimal
from .models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """A simple session-based shopping cart.

    Cart is stored in the session as {product_id (str): quantity (int)}.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        # Never let the cart quantity exceed available stock
        if self.cart[product_id] > product.quantity:
            self.cart[product_id] = product.quantity
        self.save()

    def set_quantity(self, product, quantity):
        product_id = str(product.id)
        if quantity <= 0:
            self.remove(product)
            return
        self.cart[product_id] = min(quantity, product.quantity)
        self.save()

    def increase(self, product):
        self.add(product, quantity=1)

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] -= 1
            if self.cart[product_id] <= 0:
                self.remove(product)
            else:
                self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}
        for product_id, quantity in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            yield {
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity,
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
            total += item['subtotal']
        return total
