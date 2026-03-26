# 🗺️ SYSTEM ARCHITECTURE & FLOW

## 📱 User Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SHOPCART SYSTEM                           │
└─────────────────────────────────────────────────────────────────┘

                          VISITOR
                            │
                     ┌──────┴──────┐
                     │             │
              LOGIN PAGE    BROWSE PRODUCTS
                  │              │
                  │        ┌──────┴─────────┐
              USER LOGIN  SEARCH │ FILTER │ SORT
                  │              │
                  │        ┌──────▼──────┐
              ✓ LOGIN    VIEW PRODUCTS
                  │              │
                  └──────┬───────┘
                        USER

                  ┌─────────────────────────┐
                  │    AUTHENTICATED USER    │
                  └─────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
      WISHLIST      PRODUCT DETAIL   CART
          │             │             │
    ┌─────▼─────┐  ┌────▼─────┐  ┌──▼────┐
    │ ❤️ Save   │  │⭐Reviews │  │🛒Add  │
    │ ✍️ Review │  │📸Images  │  │Update │
    │ 📋 View   │  │related   │  │Remove │
    └───────────┘  └──────────┘  └───────┘
          │             │             │
          │             │        ┌────▼────┐
          │             │        │CHECKOUT │
          │             │        └─────┬───┘
          │             │              │
          │             │    ┌─────────▼────────┐
          │             │    │ STEP 1: Address  │
          │             │    │ Select/Add       │
          │             │    └────────┬─────────┘
          │             │             │
          │             │    ┌────────▼──────────┐
          │             │    │ STEP 2: Payment   │
          │             │    │ Choose Method    │
          │             │    └────────┬──────────┘
          │             │             │
          │             │    ┌────────▼───────────┐
          │             │    │ STEP 3: Review     │
          │             │    │ Confirm Order      │
          │             │    └────────┬───────────┘
          │             │             │
          │             │    ┌────────▼──────────────┐
          │             │    │ PLACE ORDER          │
          │             │    │ Generate Order ID   │
          │             │    └────────┬─────────────┘
          │             │             │
          │             │    ┌────────▼──────────────┐
          │             │    │ ORDER CONFIRMATION   │
          │             │    │ Show Tracking Page   │
          │             │    └────────┬─────────────┘
          │             │             │
          │             │    ┌────────▼──────────────┐
          │             │    │ ORDER STATUS         │
          │             │    │ Step: 1➡️2➡️3➡️4     │
          │             │    └────────┬─────────────┘
          │             │             │
          │             │    ┌────────▼──────────────┐
          │             │    │ ORDER HISTORY        │
          │             │    │ Track All Orders     │
          │             │    └──────────────────────┘
          │             │
          └─────────────┴────────────────────────────→ REPEAT

```

---

## 🗄️ Database Schema

```
┌──────────────────────────────────────────────────────────┐
│                    DJANGO AUTH                           │
│                    ┌─────────────┐                       │
│                    │   User      │                       │
│                    └──────┬──────┘                       │
│                           │                              │
└──────────────────────────-┼──────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼─────┐    ┌──────▼──────┐  ┌──────▼──────┐
    │Cart       │    │Wishlist     │  │Address      │
    ├──────────┤    ├────────────┤  ├────────────┤
    │user (1-1)│    │user (1-1)  │  │user (1-M)  │
    │items (1-M)    │items (1-M) │  │is_default  │
    │updated_at│    │added_at    │  │phone       │
    └─────┬────┘    └─────┬──────┘  └────────────┘
          │                │
    ┌─────▼──────────┐     │
    │CartItem        │     │
    ├────────────────┤     │
    │product (FK)    │     │
    │quantity        │     │
    │added_at        │     │
    └────────────────┘     │
                           │
    ┌──────────────────────▼───────────────────┐
    │                                           │
    │         PRODUCT ECOSYSTEM                │
    │                                           │
    │  ┌─────────────┐        ┌─────────────┐  │
    │  │ Category    │        │  Product    │  │
    │  ├─────────────┤        ├─────────────┤  │
    │  │ name        │◀──────▶│ category(FK)│  │
    │  │ description │        │ price       │  │
    │  │ image       │        │ discount    │  │
    │  └─────────────┘        │ images(x4)  │  │
    │                         │ stock       │  │
    │                         │ rating      │  │
    │                         │ seller      │  │
    │                         └──────┬──────┘  │
    │                                │         │
    │                         ┌──────▼──────┐  │
    │                         │ProductReview│  │
    │                         ├─────────────┤  │
    │                         │user    (FK) │  │
    │                         │product (FK) │  │
    │                         │rating       │  │
    │                         │title        │  │
    │                         │comment      │  │
    │                         │verified     │  │
    │                         │helpful_count│  │
    │                         └─────────────┘  │
    │                                           │
    └───────────────────────────────────────────┘

    ┌───────────────────────────────────────────┐
    │                                           │
    │         ORDER SYSTEM                     │
    │                                           │
    │  ┌──────────────┐     ┌──────────────┐   │
    │  │  Order       │     │ OrderItem    │   │
    │  ├──────────────┤     ├──────────────┤   │
    │  │order_id      │────▶│order    (FK) │   │
    │  │user    (FK)  │     │product  (FK) │   │
    │  │address (FK)  │     │quantity      │   │
    │  │payment_method       │price        │   │
    │  │payment_status       │total        │   │
    │  │subtotal      │     └──────────────┘   │
    │  │tax           │                         │
    │  │shipping      │                         │
    │  │total_amount  │                         │
    │  │status        │                         │
    │  │order_date    │                         │
    │  └──────────────┘                         │
    │                                           │
    └───────────────────────────────────────────┘

```

---

## 🔄 Request Flow

```
┌────────────────┐
│  User Request  │
└────────┬───────┘
         │
    ┌────▼────────────────────────────┐
    │  Django URL Router               │
    │  (cart/urls.py)                  │
    └────┬───────────────────┬────────┘
         │                   │
    ┌────▼────────┐   ┌──────▼──────────┐
    │GET /product │   │POST /add/<id>/   │
    └────┬────────┘   └──────┬──────────┘
         │                   │
    ┌────▼──────────────┐   ┌▼─────────────────┐
    │View: product_list │   │View: add_to_cart │
    │                   │   │                  │
    │1. Query products  │   │1. Get user       │
    │2. Filter/search   │   │2. Get/create cart  │
    │3. Return template │   │3. Add cartitem   │
    └────┬──────────────┘   │4. Redirect       │
         │                  └──────┬───────────┘
    ┌────▼──────────────────┐      │
    │Render Template        │      │
    │product_list.html      │      │
    │                       │      │
    │Loop through products  │      │
    │Show images, prices    │      │
    │Links to add/wishlist  │      │
    └───┬──────────────────┘       │
        │                          │
    ┌───▼──────────────────────────▼────┐
    │ HTTP Response to Browser           │
    │ HTML with product grid             │
    └───┬───────────────────────────────┘
        │
    ┌───▼───────────────────┐
    │ User sees product list│
    │ Cart badge shows count│
    └───────────────────────┘

```

---

## 💳 Checkout process detailed

```
                    CHECKOUT START
                        │
        ┌───────────────┴────────────────┐
        │                                │
    ┌───▼──────────────┐      ┌─────────▼─────────┐
    │Cart is loaded    │      │Addresses fetched  │
    │Items validated   │      │Default selected   │
    │Totals computed   │      └────────┬──────────┘
    └────┬─────────────┘               │
         │                             │
         └────────────┬────────────────┘
                     │
            ┌────────▼──────────┐
            │STEP 1: Address    │
            │                   │
            │Display addresses  │
            │Option to add new  │
            │User selects one   │
            └────────┬──────────┘
                     │ Submit
                     │
            ┌────────▼──────────┐
            │STEP 2: Payment    │
            │                   │
            │Show payment       │
            │options:           │
            │• Card            │
            │• UPI             │
            │• Wallet          │
            │• Cash on Delivery│
            │                  │
            │User selects one  │
            └────────┬─────────┘
                     │ Submit
                     │
            ┌────────▼──────────────┐
            │STEP 3: Review         │
            │                       │
            │Show all items         │
            │Show calculations:     │
            │ Subtotal: ₹1000       │
            │ Tax (5%): ₹50         │
            │ Shipping: FREE/₹50    │
            │ TOTAL: ₹1050 or ₹1100│
            │                       │
            │User reviews          │
            │User clicks Place Order
            └────────┬──────────────┘
                     │ POST /place-order/
                     │
            ┌────────▼─────────────────────┐
            │Backend Processing            │
            │                              │
            │1. Validate cart              │
            │2. Get address & payment      │
            │3. Calculate final prices     │
            │4. Create Order object        │
            │   └─ Generate unique ID      │
            │5. Create OrderItems          │
            │6. Update product stock       │
            │7. Clear cart                 │
            │8. Redirect to confirmation   │
            └────────┬────────────────────┘
                     │
            ┌────────▼──────────────────┐
            │Confirmation Page           │
            │                           │
            │✅ Order Placed!           │
            │ Order #ORD-ABC123XY       │
            │ Total: ₹1050              │
            │ Address: [selected]       │
            │ Status Tracker: 4 steps   │
            │                           │
            │Button: View Order Details │
            │Button: Continue Shopping  │
            └─────────────────────────┘

```

---

## 📊 Review & Rating System

```
                Product Detail Page
                        │
            ┌───────────┴───────────┐
            │                       │
        ┌───▼─────────┐     ┌──────▼──────┐
        │Images       │     │Reviews      │
        │Carousel     │     │Section      │
        │4 images     │     │             │
        │             │     │Avg Rating   │
        │             │     │⭐ 4.5       │
        │             │     │(125 reviews)│
        │             │     │             │
        │             │     │Rating Bar   │
        │             │     │⭐⭐⭐⭐⭐: 50│
        │             │     │⭐⭐⭐⭐:  35│
        │             │     │⭐⭐⭐:    25│
        │             │     │⭐⭐:      10│
        │             │     │⭐:         5│
        │             │     │             │
        │             │     │Reviews List │
        │             │     │┌───────────┐│
        │             │     ││⭐⭐⭐⭐⭐ ││
        │             │     ││"Best buy" ││
        │             │     ││by username││
        │             │     ││✓ Verified ││
        │             │     ││13 helpful ││
        │             │     │└───────────┘│
        │             │     │┌───────────┐│
        │             │     ││⭐⭐⭐⭐   ││
        │             │     ││"Good but" ││
        │             │     │└───────────┘│
        │             │     │             │
        │             │     │✍️ Write Rev│
        │             │     │button       │
        │             │     └──────┬──────┘
        │             │            │
        └─────────────┴────────────┤
                                   │
                        ┌──────────▼──────────┐
                        │Modal: Write Review  │
                        │                     │
                        │Select Rating: ⭐⭐⭐│
                        │                     │
                        │Title: [text box]    │
                        │                     │
                        │Comment: [textarea]  │
                        │                     │
                        │[Submit] [Cancel]    │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │Review Posted!       │
                        │                     │
                        │Backend:             │
                        │1. Save to DB        │
                        │2. Calc new avg      │
                        │3. Update product    │
                        │4. Increment count   │
                        │5. Reload page       │
                        │                     │
                        │New rating shows ⭐.│
                        └─────────────────────┘

```

---

## 📱 Admin Dashboard Flow

```
           Admin Logs In
                │
        ┌───────┴────────┐
        │                │
    Dashboard Page
        │
        ├─ Products
        │   ├─ List all
        │   ├─ Search
        │   ├─ Filter by category/status
        │   ├─ Add new
        │   ├─ Edit existing
        │   │   ├─ Upload images
        │   │   ├─ Set prices/discounts
        │   │   ├─ Manage stock
        │   │   └─ Set seller info
        │   └─ Delete product
        │
        ├─ Orders
        │   ├─ List all orders
        │   ├─ Filter by status/date
        │   ├─ View order details
        │   ├─ Update status
        │   │   ├─ Pending
        │   │   ├─ Confirmed
        │   │   ├─ Shipped
        │   │   └─ Delivered
        │   └─ See payment status
        │
        ├─ Reviews
        │   ├─ List all reviews
        │   ├─ Filter by rating
        │   ├─ Approve/reject
        │   ├─ See verified purchases
        │   └─ Track helpful count
        │
        ├─ Categories
        │   ├─ Add category
        │   ├─ Edit name/description
        │   └─ Assign products
        │
        ├─ Users
        │   ├─ List customers
        │   ├─ View their orders
        │   └─ See cart items
        │
        └─ Reports
            ├─ Sales
            ├─ Product performance
            └─ Customer activity
```

---

## 🎯 Key Decision Points

```
User Flow Decisions:

1. Have Account?
   ├─ NO → Create account → Login
   └─ YES → Login → Browse

2. Product Interesting?
   ├─ NO → Continue browsing
   └─ YES → View details → Read reviews

3. Want to Buy?
   ├─ NO → Maybe add to wishlist
   └─ YES → Add to cart → Continue/Checkout

4. More Items?
   ├─ YES → Goto 2
   └─ NO → Proceed to checkout

5. In Checkout - Address?
   ├─ Have saved → Select it
   └─ New → Add address → Select it

6. Payment Method?
   ├─ Card → Proceed
   ├─ UPI → Proceed
   ├─ Wallet → Proceed
   └─ COD → Proceed

7. Ready to Order?
   ├─ NO → Edit cart/address
   └─ YES → Place order

8. Order Placed!
   ├─ View confirmation
   ├─ Track order
   └─ Review products (after delivery)
```

This visual architecture shows how everything connects together! 🎉
