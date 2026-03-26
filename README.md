# 🛒 ShopCart - Django Shopping Cart System

A complete, database-driven shopping cart e-commerce application built with Django. Perfect for your final-year project with all essential features implemented.

## 📋 Project Overview

**ShopCart** is a mini e-commerce web application that allows users to:
- 📦 Browse products by category
- 🔍 Search for products
- 🛍️ View product details
- 🛒 Add/remove items from cart
- 📊 Store everything in a database (SQLite by default)
- 👤 User authentication system

**No payment integration** - Focus is on cart functionality and product management.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 5.2+ |
| **Database** | SQLite (default) / PostgreSQL |
| **Frontend** | HTML5 + Bootstrap 5 |
| **Image Support** | Pillow |
| **Auth** | Django built-in user system |

---

## 📁 Project Structure

```
shoppingcart/
│
├── manage.py                 # Django management script
├── cart/                     # Main app folder
│   ├── models.py            # Database models
│   ├── views.py             # View functions (product, cart logic)
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── migrations/          # Database migrations
│   └── tests.py             # Unit tests
│
├── cart_proj/               # Project settings folder
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
│
├── templates/               # HTML templates
│   ├── cart/
│   │   ├── base.html        # Base template
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   └── cart.html
│   └── registration/
│       └── login.html
│
├── media/                   # User-uploaded files (images)
├── db.sqlite3              # SQLite database
└── .venv/                  # Virtual environment
```

---

## 🗄️ Database Models

### **Category**
```python
- id (auto)
- name (max 100 chars)
- created_at (timestamp)
```

### **Product**
```python
- id (auto)
- name (max 200 chars)
- description (text)
- price (float)
- category (ForeignKey → Category)
- image (optional, uploaded to media/products/)
- created_at, updated_at (timestamps)
```

### **Cart**
```python
- id (auto)
- user (OneToOneField → User)
- created_at, updated_at (timestamps)
```

### **CartItem**
```python
- id (auto)
- cart (ForeignKey → Cart)
- product (ForeignKey → Product)
- quantity (integer, default=1)
- added_at (timestamp)
```

---

## 🚀 Getting Started

### 1️⃣ **Activate Virtual Environment**

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 2️⃣ **Install Required Packages** (if needed)

```bash
pip install django pillow
```

### 3️⃣ **Run Development Server**

```bash
python manage.py runserver
```

Server runs at: **http://127.0.0.1:8000**

### 4️⃣ **Access Admin Panel**

```
URL: http://127.0.0.1:8000/admin
Username: admin
Password: (you'll be prompted to set this)
```

### 5️⃣ **Add Sample Data via Admin**

1. Login to admin panel
2. Click on "Categories" → Add categories (Electronics, Clothing, Books, etc.)
3. Click on "Products" → Add products with prices, descriptions, and images
4. Test the shopping cart with user account

---

## 🎯 Core Features Implemented

### ✅ **1. Product Listing**
- Display all products in a responsive grid
- Pagination support
- Product cards with name, price, and image

### ✅ **2. Category Filtering**
- Filter products by category
- Sidebar navigation with category links
- "All Categories" option to view all

### ✅ **3. Search Functionality**
- Search by product name or description
- Real-time search form on product list
- Clear filters button

### ✅ **4. Product Detail Page**
- Full product information
- Product image display
- Related products section
- Add to cart button

### ✅ **5. Shopping Cart**
- View all cart items
- Update quantity for each item
- Remove items from cart
- Calculate total price
- Cart item count badge in navbar

### ✅ **6. User Authentication**
- Login system (Django built-in)
- Protected cart views (login required)
- User-specific cart isolation
- Logout functionality

### ✅ **7. Admin Panel**
- Manage categories
- Add/edit/delete products
- Upload product images
- View all carts and cart items
- Search and filtering capabilities

---

## 🔐 User Workflow

```
Visitor (Unauthenticated)
    ↓
    Can browse products & search
    ↓
    Click "Add to Cart" → Redirected to Login
    ↓
Logged-in User
    ↓
    Add products to cart
    ↓
    View cart
    ↓
    Update quantities
    ↓
    Remove items
    ↓
    View total price
```

---

## 📝 Admin Use Cases

### **Add a New Product:**
1. Go to `/admin`
2. Click "Products"
3. Click "Add Product +"
4. Fill: Name, Description, Price, Category
5. Optional: Upload product image
6. Click "Save"

### **Add a Category:**
1. Go to `/admin`
2. Click "Categories"
3. Click "Add Category +"
4. Enter category name (e.g., "Electronics")
5. Click "Save"

### **View Customer Carts:**
1. Go to `/admin`
2. Click "Carts" to see all user carts
3. Click on a cart to see cart items
4. View total price and item details

---

## 🌐 URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/` | `product_list` | Home page - all products |
| `/product/<id>/` | `product_detail` | Product detail page |
| `/add/<product_id>/` | `add_to_cart` | Add product to cart |
| `/cart/` | `cart_view` | View shopping cart |
| `/remove/<item_id>/` | `remove_from_cart` | Remove item from cart |
| `/update/<item_id>/` | `update_cart_quantity` | Update cart item quantity |
| `/admin/` | Django Admin | Admin panel |
| `/accounts/login/` | Django Auth | Login page |
| `/accounts/logout/` | Django Auth | Logout |

---

## 🎨 Frontend Features

### **Bootstrap 5 Styling**
- Responsive design (mobile, tablet, desktop)
- Professional dark navbar with logo
- Product cards with hover effects
- Detailed product images
- Clean cart layout

### **User Interface**
- Search bar for quick product discovery
- Category filter sidebar
- Product image thumbnails
- Shopping cart badge with item count
- Quick actions (Add to Cart, View, Remove)

### **Navigation**
- Navbar with links to products and cart
- Breadcrumb navigation on product detail page
- Back buttons for easy navigation
- Related products recommendations

---

## 🧪 Testing the Application

### **Test Scenario 1: Browse Products**
```
1. Go to http://127.0.0.1:8000
2. See all products displayed
3. Use search bar to find a product
4. Click on category to filter
5. Verify correct filtering
```

### **Test Scenario 2: Add to Cart**
```
1. Click "Add to Cart" on any product
2. Login with credentials (if not logged in)
3. Redirected to cart page
4. See product in cart with quantity
5. Verify total price is calculated
```

### **Test Scenario 3: Update Quantity**
```
1. Change quantity in cart
2. Form auto-submits
3. Verify total updates
4. Remove item - verify it disappears
```

### **Test Scenario 4: Multiple Products**
```
1. Add different products to cart
2. Verify each appears separately
3. Check total is sum of all items
4. Check cart badge updates
```

---

## 🔄 Database Migrations

The following migrations have been applied:

```
✓ contenttypes.0001_initial
✓ auth.0001_initial (Django auth system)
✓ admin.0001_initial (Django admin)
✓ cart.0001_initial (Category, Product, Cart, CartItem models)
✓ sessions.0001_initial (User sessions)
```

To create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ⚙️ Configuration

### **Media Files (Product Images)**
- Upload directory: `media/products/`
- Supported formats: JPG, PNG, GIF, WebP
- Max file size: Configurable in settings

### **Static Files**
- CSS, JS, Images: `static/`
- Bootstrap CDN used for styling
- Collect static files for production:
```bash
python manage.py collectstatic
```

### **Database Settings** (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To use PostgreSQL, update settings.py DATABASES configuration.

---

## 🛑 Important Notes for Demo/Viva

### **Features to Highlight:**

1. **Database Design**
   - Relational schema with ForeignKeys
   - User-to-Cart relationship
   - Category-to-Product relationship

2. **CRUD Operations**
   - Create: Add products via admin (→ product appears on list)
   - Read: View products, cart items
   - Update: Modify quantities in cart
   - Delete: Remove products/items

3. **Business Logic**
   - Unique cart per user (OneToOne)
   - Prevent duplicate items (unique constraint on cart, product)
   - Auto-calculate totals
   - Related products recommendations

4. **Security**
   - Login required for cart operations
   - User isolation (can't see other users' carts)
   - CSRF protection on forms

5. **User Experience**
   - Responsive design
   - Search functionality
   - Category filtering
   - Clear error messages

### **Demo Commands to Run:**

```bash
# Start server
python manage.py runserver

# Create admin account (if needed)
python manage.py createsuperuser

# Add test data via shell
python manage.py shell
>>> from cart.models import Category, Product
>>> c = Category.objects.create(name="Electronics")
>>> p = Product.objects.create(name="Laptop", price=999, description="High performance laptop", category=c)
>>> exit()

# Check database
python manage.py dbshell
> SELECT * FROM cart_product;
```

---

## 📚 Extra Features (Optional - for Higher Marks)

If you want to extend this project:

- [ ] **Wishlist** - Save favorite products
- [ ] **Product Reviews** - User ratings and comments
- [ ] **Order History** - Track user purchases
- [ ] **Pagination** - Limit products per page
- [ ] **AJAX** - Dynamic add to cart without reload
- [ ] **REST API** - Django REST Framework
- [ ] **Email Notifications** - Order confirmations
- [ ] **Payment Integration** - Stripe/PayPal (if adding payment)
- [ ] **Inventory Management** - Stock tracking
- [ ] **Admin Dashboard** - Sales analytics

---

## 🐛 Troubleshooting

### **Django not found**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### **Database errors**
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### **Images not displaying**
```python
# In settings.py, check:
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# In main urls.py:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### **Port already in use**
```bash
# Use different port
python manage.py runserver 8001
```

---

## 📞 Support & Resources

- **Django Docs**: https://docs.djangoproject.com
- **Bootstrap Docs**: https://getbootstrap.com
- **Django Models**: https://docs.djangoproject.com/en/5.2/topics/db/models/
- **Django Admin**: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/

---

## 📜 License

This project is for educational purposes. Use freely for your final-year project.

---

**Happy Coding! 🚀**

Good luck with your viva and project demo! Make sure to:
- Add 15-20 test products via admin
- Have sample categories set
- Demo search and filtering
- Show cart operations with multiple items
- Highlight the database design during viva
