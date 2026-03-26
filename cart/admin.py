from django.contrib import admin
from .models import (
    Category, Product, ProductReview, Cart, CartItem, 
    Wishlist, WishlistItem, Address, Order, OrderItem, Coupon
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'get_discount_percent', 'stock', 'rating', 'review_count']
    list_filter = ['category', 'stock_status', 'rating', 'free_shipping', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'rating', 'review_count']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'seller')
        }),
        ('Pricing & Discount', {
            'fields': ('price', 'discount_price',)
        }),
        ('Images', {
            'fields': ('image', 'image2', 'image3', 'image4'),
            'classes': ('collapse',)
        }),
        ('Inventory', {
            'fields': ('stock', 'stock_status', 'free_shipping')
        }),
        ('Ratings', {
            'fields': ('rating', 'review_count'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_discount_percent(self, obj):
        return f"{obj.get_discount_percent()}%"
    get_discount_percent.short_description = "Discount %"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'verified_purchase', 'helpful_count', 'created_at']
    list_filter = ['rating', 'verified_purchase', 'created_at']
    search_fields = ['user__username', 'product__name', 'title', 'comment']
    readonly_fields = ['created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = "Total Items"

    def get_total_price(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'get_item_total']
    list_filter = ['added_at']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['added_at']

    def get_item_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_item_total.short_description = "Item Total"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_item_count', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

    def get_item_count(self, obj):
        return obj.items.count()
    get_item_count.short_description = "Items Count"


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'wishlist', 'added_at']
    search_fields = ['product__name', 'wishlist__user__username']
    readonly_fields = ['added_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'city', 'state', 'is_default', 'created_at']
    list_filter = ['address_type', 'is_default', 'state', 'created_at']
    search_fields = ['user__username', 'city', 'street_address']
    readonly_fields = ['created_at']
    fieldsets = (
        ('User', {
            'fields': ('user', 'is_default')
        }),
        ('Address', {
            'fields': ('address_type', 'street_address', 'apartment', 'city', 'state', 'zip_code', 'country', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'status', 'payment_status', 'total_amount', 'order_date']
    list_filter = ['status', 'payment_status', 'payment_method', 'order_date']
    search_fields = ['order_id', 'user__username']
    readonly_fields = ['order_id', 'order_date', 'shipped_date', 'delivered_date']
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_id', 'user', 'status', 'order_date')
        }),
        ('Shipping', {
            'fields': ('address', 'shipped_date', 'delivered_date')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax', 'shipping_cost', 'coupon_discount', 'total_amount')
        }),
        ('Notes', {
            'fields': ('special_instructions',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__order_date']
    search_fields = ['product__name', 'order__order_id']
    readonly_fields = ['order', 'product', 'quantity', 'price']

    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = "Total"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'min_purchase', 'is_active', 'used_count', 'expiry_date']
    list_filter = ['is_active', 'expiry_date', 'created_at']
    search_fields = ['code', 'description']
    readonly_fields = ['created_at', 'used_count']


