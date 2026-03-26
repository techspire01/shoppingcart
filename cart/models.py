from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


# =========== BASIC MODELS ===========
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Product(models.Model):
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    discount_price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='products/', null=True, blank=True)
    image4 = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField(default=0)
    seller = models.CharField(max_length=100, default='ShopCart Store')
    free_shipping = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_avg_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg if avg else 0

    def get_discount_percent(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def get_current_price(self):
        return self.discount_price if self.discount_price else self.price

    class Meta:
        ordering = ['-created_at']


# =========== REVIEW & RATING ===========
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    comment = models.TextField()
    helpful_count = models.IntegerField(default=0)
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']


# =========== WISHLIST ===========
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"

    class Meta:
        unique_together = ('wishlist', 'product')


# =========== CART ===========
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_subtotal(self):
        return sum(item.get_total() for item in self.items.all())

    def get_total_with_tax(self):
        subtotal = self.get_subtotal()
        tax = round(subtotal * 0.05, 2)  # 5% tax
        shipping = 0 if subtotal > 500 else 50  # Free shipping over 500
        return round(subtotal + tax + shipping, 2)

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def get_total(self):
        return self.product.get_current_price() * self.quantity

    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-added_at']


# =========== ADDRESS ===========
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=[('home', 'Home'), ('office', 'Office')], default='home')
    street_address = models.CharField(max_length=200)
    apartment = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    phone = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"

    class Meta:
        ordering = ['-is_default', '-created_at']


# =========== ORDER ===========
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('wallet', 'Digital Wallet'),
        ('cod', 'Cash on Delivery'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    
    subtotal = models.FloatField()
    shipping_cost = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    coupon_discount = models.FloatField(default=0, null=True, blank=True)
    total_amount = models.FloatField()
    
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    special_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            import uuid
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} in Order #{self.order.order_id}"

    def get_total(self):
        return self.quantity * self.price


# =========== COUPON ===========
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_purchase = models.FloatField(default=0)
    max_usage = models.IntegerField(default=1000)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-created_at']

