# ⚡ Quick Start Guide - ShopCart

## 🚀 30-Second Setup

1. **Activate Virtual Environment**
   ```bash
   .venv\Scripts\activate
   ```

2. **Start Server**
   ```bash
   python manage.py runserver
   ```

3. **Open Browser**
   - Visit: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin
   - Username: `admin`

---

## 📋 First-Time Setup Checklist

- [x] Models created (Category, Product, Cart, CartItem)
- [x] Migrations applied
- [x] Superuser created (`admin`)
- [x] Templates ready
- [x] Views configured
- [x] URLs routed

✅ **Everything is ready to use!**

---

## 👨‍💼 Admin Panel Tasks

### Add Categories
1. Go to `/admin`
2. Click "Categories" → "Add Category"
3. Enter name (e.g., "Electronics", "Books")
4. Click "Save"

### Add Products
1. Go to `/admin`
2. Click "Products" → "Add Product"
3. Fill in:
   - Name: Product name
   - Description: Product details
   - Price: Product price
   - Category: Select category
   - Image: Optional product image
4. Click "Save"

**Tip:** Add 15-20 products for a good demo!

---

## 🧑‍💻 Test User Account

Create a test user to test the shopping cart:

```bash
python manage.py createsuperuser
# or use the existing admin account to browse
```

Then login and:
1. Browse products
2. Search for a product
3. Add to cart
4. View cart
5. Update quantities
6. Remove items

---

## 🔗 Important URLs

| URL | Purpose |
|-----|---------|
| `/` | Product listing (home) |
| `/admin/` | Admin panel |
| `/accounts/login/` | Login page |
| `/cart/` | Shopping cart |
| `/product/<id>/` | Product detail |

---

## 📊 For Your Viva Preparation

### Key Points to Explain:

1. **Models Relationship**
   ```
   Category ← Product ← CartItem → Cart → User
   ```

2. **User Isolation**
   - Each user has ONE cart (OneToOne relationship)
   - Can't see other carts

3. **Cart Logic**
   - Add product: Gets or creates CartItem with quantity
   - Update: Increment quantity if already in cart
   - Remove: Delete CartItem from cart

4. **Search & Filter**
   - Search: Uses Q objects for name OR description
   - Filter: By category ID from GET parameters

5. **Security**
   - `@login_required` decorator on cart views
   - CSRF tokens on forms
   - Templates check `user.is_authenticated`

---

## 🐛 Quick Fixes

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Reinstall Dependencies
```bash
pip install --upgrade django pillow
```

### Check Configuration
```bash
python manage.py check
```

---

## 💡 Demo Script for Viva

```
1. "Let me show you the database schema first..."
   → Show models in admin
   
2. "Here's a product with details..."
   → Show product_detail page
   
3. "I can search across products..."
   → Demo search functionality
   
4. "Filter by category..."
   → Demo category filter
   
5. "Login and add to cart..."
   → Demo add_to_cart
   
6. "View the shopping cart..."
   → Show cart with items, total, and operations
   
7. "Update quantities..."
   → Demo quantity update
   
8. "And remove items..."
   → Demo remove from cart
```

---

## 📦 Project Files Created

```
✓ cart/models.py          - Database models
✓ cart/views.py           - View functions
✓ cart/urls.py            - URL routing
✓ cart/admin.py           - Admin configuration
✓ templates/cart/base.html                - Base template
✓ templates/cart/product_list.html        - Products page
✓ templates/cart/product_detail.html      - Product details
✓ templates/cart/cart.html                - Shopping cart
✓ templates/registration/login.html       - Login page
✓ cart_proj/settings.py   - Settings updated
✓ cart_proj/urls.py       - Main URLs updated
✓ Migrations              - Database schema applied
```

---

## 🎓 Learning Points

This project demonstrates:

- ✅ Django ORM (Models, Relationships)
- ✅ URL Routing & Views
- ✅ Database Queries (Get, Create, Filter)
- ✅ User Authentication
- ✅ Django Admin
- ✅ Form Handling & CSRF
- ✅ Template Rendering
- ✅ Static Files & Media
- ✅ Bootstrap Integration
- ✅ Business Logic (Cart calculations)

---

## 🚀 Next Steps (Optional)

Want to extend? Try adding:
- Payment gateway (Stripe)
- Order history
- Product reviews
- Wishlist
- Email notifications
- REST API with DRF

---

**Everything is set up and ready for demo! 🎉**

Need help? Check the README.md for detailed documentation.
