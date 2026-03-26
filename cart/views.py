from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime
import json

from .models import (
    Product, Category, Cart, CartItem, ProductReview, 
    Wishlist, WishlistItem, Order, OrderItem, Address, Coupon
)


# =========== PRODUCT BROWSING ===========
def product_list(request):
    """Display list of products with search, filter, and sorting"""
    products = Product.objects.all()
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))

    # Rating filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        products = products.filter(rating__gte=float(min_rating))

    # Stock status
    stock_status = request.GET.get('stock')
    if stock_status == 'in_stock':
        products = products.filter(stock__gt=0)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', 'price', '-price', '-rating', 'name']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)  # 12 products per page
    products_page = paginator.get_page(page)

    context = {
        'products': products_page,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'sort_by': sort_by,
    }
    return render(request, 'cart/product_list.html', context)


def product_detail(request, id):
    """Display detailed view of a single product with reviews"""
    product = get_object_or_404(Product, id=id)
    reviews = product.reviews.all()
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=id)[:5]
    
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        wishlist_item = WishlistItem.objects.filter(
            wishlist__user=request.user,
            product=product
        ).exists()
    else:
        wishlist_item = False

    # Calculate review stats
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_distribution = {i: reviews.filter(rating=i).count() for i in range(1, 6)}

    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
        'related_products': related_products,
        'in_wishlist': wishlist_item,
    }
    return render(request, 'cart/product_detail.html', context)


# =========== REVIEWS ===========
@login_required(login_url='login')
@require_POST
def add_review(request, product_id):
    """Add or update product review"""
    product = get_object_or_404(Product, id=product_id)
    
    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')
    
    review, created = ProductReview.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            'rating': rating,
            'title': title,
            'comment': comment,
            'verified_purchase': True,  # Check if user bought this
        }
    )
    
    # Update product rating
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    product.rating = round(avg_rating, 1)
    product.review_count = product.reviews.count()
    product.save()
    
    messages.success(request, 'Review posted successfully!')
    return redirect('product_detail', id=product_id)


# =========== WISHLIST ===========
@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        messages.success(request, f"{product.name} added to wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist!")
    
    return redirect('product_detail', id=product_id)


@login_required(login_url='login')
def wishlist_view(request):
    """Display user's wishlist"""
    try:
        wishlist = request.user.wishlist
        items = wishlist.items.all()
    except Wishlist.DoesNotExist:
        wishlist = None
        items = []
    
    context = {
        'wishlist': wishlist,
        'items': items,
    }
    return render(request, 'cart/wishlist.html', context)


@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    """Remove item from wishlist"""
    item = get_object_or_404(WishlistItem, id=item_id)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"{product_name} removed from wishlist!")
    return redirect('wishlist')


# =========== CART ===========
@login_required(login_url='login')
def add_to_cart(request, product_id):
    """Add product to cart or increase quantity"""
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock <= 0:
        messages.error(request, 'Product is out of stock!')
        return redirect('product_detail', id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, 'Cannot add more - insufficient stock!')
            return redirect('cart')
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')


@login_required(login_url='login')
def cart_view(request):
    """Display user's shopping cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        items = []
    
    subtotal = sum(item.get_total() for item in items) if items else 0.00
    tax = round(subtotal * 0.05, 2)
    shipping = 0 if subtotal > 500 else 50
    total = round(subtotal + tax + shipping, 2)
    
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(CartItem, id=item_id)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"{product_name} removed from cart!")
    return redirect('cart')


@login_required(login_url='login')
def update_cart_quantity(request, item_id):
    """Update quantity of cart item"""
    item = get_object_or_404(CartItem, id=item_id)
    
    if request.POST:
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity > 0 and quantity <= item.product.stock:
                item.quantity = quantity
                item.save()
                messages.success(request, 'Quantity updated!')
            elif quantity <= 0:
                item.delete()
            else:
                messages.error(request, 'Not enough stock available!')
        except ValueError:
            messages.error(request, 'Invalid quantity!')
    
    return redirect('cart')


# =========== CHECKOUT & ADDRESS ===========
@login_required(login_url='login')
def address_list(request):
    """Display user's saved addresses"""
    addresses = Address.objects.filter(user=request.user)
    context = {
        'addresses': addresses,
    }
    return render(request, 'cart/address_list.html', context)


@login_required(login_url='login')
def add_address(request):
    """Add new delivery address"""
    if request.POST:
        street = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        address_type = request.POST.get('address_type', 'home')
        
        address = Address.objects.create(
            user=request.user,
            street_address=street,
            apartment=apartment,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            address_type=address_type,
        )
        
        messages.success(request, 'Address added successfully!')
        return redirect('checkout')
    
    return render(request, 'cart/add_address.html')


@login_required(login_url='login')
def checkout(request):
    """Checkout page - select address and payment"""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('home')
    
    if not items:
        messages.error(request, 'Your cart is empty!')
        return redirect('home')
    
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    
    subtotal = sum(item.get_total() for item in items)
    tax = round(subtotal * 0.05, 2)
    shipping = 0 if subtotal > 500 else 50
    total = round(subtotal + tax + shipping, 2)
    
    payment_methods = [
        ('card', '💳 Credit/Debit Card'),
        ('upi', '📱 UPI'),
        ('wallet', '👜 Digital Wallet'),
        ('cod', '🚚 Cash on Delivery'),
    ]
    
    context = {
        'cart': cart,
        'items': items,
        'addresses': addresses,
        'default_address': default_address,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
        'payment_methods': payment_methods,
    }
    return render(request, 'cart/checkout.html', context)


@login_required(login_url='login')
@require_POST
def place_order(request):
    """Place order and process payment"""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, 'Cart not found!')
        return redirect('cart')
    
    if not items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    address_id = request.POST.get('address')
    if not address_id:
        messages.error(request, 'Please select a delivery address!')
        return redirect('checkout')
    
    payment_method = request.POST.get('payment_method', 'cod')
    
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        messages.error(request, 'Invalid address selected!')
        return redirect('checkout')
    
    # Calculate totals
    subtotal = sum(item.get_total() for item in items)
    tax = round(subtotal * 0.05, 2)
    shipping = 0 if subtotal > 500 else 50
    total = round(subtotal + tax + shipping, 2)
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        address=address,
        payment_method=payment_method,
        payment_status='completed' if payment_method != 'cod' else 'pending',
        subtotal=subtotal,
        tax=tax,
        shipping_cost=shipping,
        total_amount=total,
        status='confirmed',
    )
    
    # Create order items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.get_current_price(),
        )
        
        # Update stock
        item.product.stock -= item.quantity
        if item.product.stock == 0:
            item.product.stock_status = 'out_of_stock'
        elif item.product.stock < 5:
            item.product.stock_status = 'low_stock'
        item.product.save()
    
    # Clear cart
    cart.items.all().delete()
    
    messages.success(request, 'Order placed successfully!')
    return redirect('order_confirmation', order_id=order.id)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart/order_confirmation.html', context)


# =========== ORDER HISTORY ===========
@login_required(login_url='login')
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'cart/order_history.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart/order_detail.html', context)


