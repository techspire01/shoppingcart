# 📚 CODE REFERENCE - Key Implementation Details

## 🗄️ Models Overview

### Product Model (Enhanced)
```python
# Supports discounts, multiple images, ratings
price = 5000
discount_price = 3500  # Shows 30% OFF
get_discount_percent() → 30
get_current_price() → 3500

stock_status choices:
- 'in_stock'
- 'low_stock' 
- 'out_of_stock'

Multiple images: image, image2, image3, image4
Rating auto-calculated from reviews
```

### Review Model
```python
# 5-star rating system
rating = 5  # 1-5
title = "Excellent product!"
comment = "Very satisfied..."
verified_purchase = True
helpful_count = 15
user = ForeignKey(User)
product = ForeignKey(Product)
# Unique constraint on (user, product) = one review per user/product
```

### Order Model
```python
order_id = "ORD-ABC123XY"  # Auto-generated unique
user = ForeignKey(User)
address = ForeignKey(Address)
payment_method = 'cod'  # 'card', 'upi', 'wallet', 'cod'
payment_status = 'completed'  # 'pending', 'completed', 'failed'

Pricing:
- subtotal = sum of items
- tax = subtotal * 0.05 (5%)
- shipping_cost = 0 if subtotal > 500 else 50
- total_amount = subtotal + tax + shipping

Status: 'pending' → 'confirmed' → 'shipped' → 'delivered'
```

---

## 🔄 Key Views Logic

### Add to Cart
```python
@login_required
def add_to_cart(request, product_id):
    product = Product.get_or_404(product_id)
    
    # Stock validation
    if product.stock <= 0:
        error("Out of stock!")
    
    # Get or create cart
    cart = Cart.get_or_create(user=request.user)
    
    # Get or create cart item
    item, created = CartItem.get_or_create(
        cart=cart, product=product
    )
    
    # Increment quantity (don't exceed stock)
    if not created:
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()
    
    redirect('cart')
```

### Place Order Flow
```python
@login_required
@require_POST
def place_order(request):
    # 1. Get user's cart
    cart = Cart.get(user=request.user)
    items = cart.items.all()
    
    # 2. Get selected address
    address = Address.get(id=request.POST['address'])
    
    # 3. Calculate totals
    subtotal = sum(item.get_total() for item in items)
    tax = round(subtotal * 0.05, 2)
    shipping = 0 if subtotal > 500 else 50
    total = subtotal + tax + shipping
    
    # 4. Create order with auto-generated ID
    order = Order.create(
        user=request.user,
        address=address,
        subtotal=subtotal,
        tax=tax,
        shipping_cost=shipping,
        total_amount=total,
        payment_method=request.POST['payment_method'],
        status='confirmed'
    )
    
    # 5. Create order items
    for item in items:
        OrderItem.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.get_current_price()
        )
        
        # 6. Update product stock
        item.product.stock -= item.quantity
        item.product.save()
    
    # 7. Clear cart
    cart.items.all().delete()
    
    # 8. Redirect to confirmation
    redirect('order_confirmation', order.id)
```

### Review System
```python
@login_required
@require_POST
def add_review(request, product_id):
    product = Product.get_or_404(product_id)
    
    # Create or update review (unique per user-product)
    review, created = ProductReview.update_or_create(
        user=request.user,
        product=product,
        defaults={
            'rating': int(request.POST['rating']),
            'title': request.POST['title'],
            'comment': request.POST['comment'],
            'verified_purchase': True
        }
    )
    
    # Update product's avg rating
    avg_rating = product.reviews.aggregate(
        Avg('rating')
    )['rating__avg'] or 0
    
    product.rating = round(avg_rating, 1)
    product.review_count = product.reviews.count()
    product.save()
```

---

## 🎯 Pricing Calculations

### Cart Totals
```python
def get_cart_totals(cart):
    items = cart.items.all()
    
    # Subtotal
    subtotal = sum(
        item.quantity * item.product.get_current_price()
        for item in items
    )
    
    # Tax (5%)
    tax = round(subtotal * 0.05, 2)
    
    # Shipping (Free if > 500)
    shipping = 0 if subtotal > 500 else 50
    
    # Total
    total = subtotal + tax + shipping
    
    return {
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total
    }
```

### Discount Calculation
```python
def get_discount_percent(product):
    if product.discount_price:
        diff = product.price - product.discount_price
        percent = (diff / product.price) * 100
        return int(percent)
    return 0

def get_current_price(product):
    return product.discount_price or product.price
```

---

## 🌐 URL Patterns

### Shopping Routes
```python
# Browse
path('', views.product_list, name='home')
path('product/<int:id>/', views.product_detail)

# Wishlist
path('wishlist/', views.wishlist_view)
path('wishlist/add/<int:product_id>/', views.add_to_wishlist)
path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist)

# Cart
path('cart/', views.cart_view)
path('add/<int:product_id>/', views.add_to_cart)
path('update/<int:item_id>/', views.update_cart_quantity)
path('remove/<int:item_id>/', views.remove_from_cart)
```

### Checkout Routes
```python
# Addresses
path('address/', views.address_list)
path('address/add/', views.add_address)

# Checkout
path('checkout/', views.checkout)
path('place-order/', views.place_order)
path('order-confirmation/<int:order_id>/', 
     views.order_confirmation)

# Orders
path('orders/', views.order_history)
path('order/<int:order_id>/', views.order_detail)
```

---

## 📱 Template Key Sections

### Product Detail - Reviews Section
```html
<!-- Rating Summary -->
<h2>{{ avg_rating|floatformat:1 }} ⭐</h2>
<small>({{ total_reviews }} reviews)</small>

<!-- Rating Distribution -->
{% for rating in "54321" %}
    {% with count=rating_distribution|add:rating %}
        <div class="progress">
            <div class="progress-bar" 
                 style="width: {{ count|mul:100|div:total_reviews }}%">
            </div>
        </div>
    {% endwith %}
{% endfor %}

<!-- Reviews List -->
{% for review in reviews %}
    <div class="review-card">
        ⭐ {{ review.rating }}
        <strong>{{ review.title }}</strong>
        {{ review.comment }}
        {% if review.verified_purchase %}
            ✓ Verified Purchase
        {% endif %}
        {{ review.created_at|date:"M d, Y" }}
    </div>
{% endfor %}
```

### Checkout - 3-Step Process
```html
<!-- Step 1: Address -->
<div class="checkout-step active">
    <h5>1️⃣ Delivery Address</h5>
    {% for address in addresses %}
        <div class="form-check">
            <input type="radio" name="address" 
                   value="{{ address.id }}" {% if default_address == address %}checked{% endif %}>
            <label>{{ address }}</label>
        </div>
    {% endfor %}
    <a href="/address/add/">+ Add New Address</a>
</div>

<!-- Step 2: Payment -->
<div class="checkout-step">
    <h5>2️⃣ Payment Method</h5>
    <input type="radio" name="payment_method" value="cod" checked>
    Cash on Delivery
    <input type="radio" name="payment_method" value="card">
    Credit/Debit Card
</div>

<!-- Step 3: Review -->
<div class="checkout-step">
    <h5>3️⃣ Order Review</h5>
    <table>
        {% for item in items %}
            <tr>
                <td>{{ item.product.name }}</td>
                <td>₹{{ item.product.get_current_price }}</td>
                <td>{{ item.quantity }}</td>
                <td>₹{{ item.get_total }}</td>
            </tr>
        {% endfor %}
    </table>
</div>
```

### Order Tracking
```html
<!-- 4-Step Status -->
<div class="order-tracker">
    {% for step in steps %}
        <div class="step {% if step.active %}active{% endif %}">
            <div class="step-number">{{ step.number }}</div>
            <p>{{ step.name }}</p>
            {% if step.date %}<small>{{ step.date }}</small>{% endif %}
        </div>
    {% endfor %}
</div>

Steps:
1. ✅ Confirmed {{ order.order_date|date }}
2. 📦 Shipped {{ order.shipped_date|date }}
3. 🚚 Out for Delivery
4. ✅ Delivered {{ order.delivered_date|date }}
```

---

## 🔑 Database Queries Used

```python
# Filter by category
Product.objects.filter(category__name='Electronics')

# Search across fields
Product.objects.filter(
    Q(name__icontains=query) | 
    Q(description__icontains=query)
)

# Get user's cart
Cart.objects.get_or_create(user=user)

# Get user's wishlist
Wishlist.objects.get_or_create(user=user)

# Avg rating of product
Product.objects.annotate(
    avg_rating=Avg('reviews__rating')
)

# Orders filtered by user
Order.objects.filter(user=user).order_by('-order_date')

# Get order with items
order = Order.objects.get(id=order_id)
items = order.items.all()

# Get user reviews
reviews = ProductReview.objects.filter(
    user=user, 
    product=product
).unique()
```

---

## 🎨 Bootstrap Classes Used

```html
<!-- Cards -->
<div class="card">
    <div class="card-header bg-primary text-white"></div>
    <div class="card-body"></div>
    <div class="card-footer"></div>
</div>

<!-- Badges -->
<span class="badge bg-success">In Stock</span>
<span class="badge bg-danger">30% OFF</span>

<!-- Forms -->
<form method="POST">
    {% csrf_token %}
    <input class="form-control">
    <button class="btn btn-primary">Submit</button>
</form>

<!-- Tables -->
<div class="table-responsive">
    <table class="table table-striped">...</table>
</div>

<!-- Modal -->
<div class="modal fade" id="reviewModal">
    <div class="modal-dialog">
        <div class="modal-content">...</div>
    </div>
</div>
```

---

## 🚀 Important Settings

```python
# settings.py

INSTALLED_APPS = [
    ...
    'cart',
]

TEMPLATES['DIRS'] = [BASE_DIR / 'templates']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# In main urls.py
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
```

---

## 🧪 Test Commands

```bash
# Create superuser
python manage.py createsuperuser

# Add test data via shell
python manage.py shell

# In shell:
from cart.models import *
cat = Category.objects.create(name="Electronics")
prod = Product.objects.create(name="Phone", price=10000, category=cat)
```

---

**This covers all major implementation details! 🎉**
