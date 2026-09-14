import uuid
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category, Order
from .cart import Cart
from .forms import CheckoutForm


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:8]
    if not featured_products:
        featured_products = Product.objects.all()[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'shop/products.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.add(product, quantity=1)
    messages.success(request, f'"{product.name}" added to your cart.')
    next_url = request.POST.get('next') or request.GET.get('next') or 'product_list'
    return redirect(next_url)


def cart_increase(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.increase(product)
    return redirect('cart_detail')


def cart_decrease(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.decrease(product)
    return redirect('cart_detail')


def cart_set_quantity(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        cart.set_quantity(product, quantity)
    return redirect('cart_detail')


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    messages.info(request, f'"{product.name}" removed from your cart.')
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add some products first.")
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            customer = form.save()
            order_group = uuid.uuid4().hex[:12]

            for item in cart:
                product = item['product']
                quantity = item['quantity']
                Order.objects.create(
                    customer=customer,
                    product=product,
                    quantity=quantity,
                    total_price=item['subtotal'],
                    order_group=order_group,
                )
                # Reduce stock
                product.quantity = max(product.quantity - quantity, 0)
                product.save()

            cart.clear()
            request.session['last_order_group'] = order_group
            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})


def order_success(request):
    order_group = request.session.pop('last_order_group', None)
    orders = Order.objects.filter(order_group=order_group) if order_group else []
    total = sum((o.total_price for o in orders), start=0)
    return render(request, 'shop/order_success.html', {'orders': orders, 'total': total})
