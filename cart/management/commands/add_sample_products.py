from django.core.management.base import BaseCommand
from cart.models import Category, Product


class Command(BaseCommand):
    help = 'Add 20 sample products from various categories'

    def handle(self, *args, **options):
        # Create categories
        categories_data = {
            'Electronics': 'Electronic devices and gadgets',
            'Fashion': 'Clothing and accessories',
            'Home & Kitchen': 'Home appliances and kitchen items',
            'Books': 'Physical and digital books',
            'Sports': 'Sports equipment and gear'
        }

        categories = {}
        for cat_name, cat_desc in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'created_at': None}
            )
            categories[cat_name] = category
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {cat_name}')
                )
            else:
                self.stdout.write(f'• Category already exists: {cat_name}')

        # Sample products data
        products_data = [
            # Electronics (5 products)
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'Premium wireless headphones with noise cancellation, 30-hour battery life, and crystal-clear sound quality.',
                'price': 4999,
                'discount_price': 3499,
                'category': 'Electronics',
                'stock': 15,
                'seller': 'TechStore Pro',
                'free_shipping': True,
                'rating': 4.5,
                'review_count': 342
            },
            {
                'name': 'USB-C Fast Charging Cable',
                'description': 'Durable USB-C cable with fast charging support up to 100W, compatible with all USB-C devices.',
                'price': 599,
                'discount_price': 349,
                'category': 'Electronics',
                'stock': 50,
                'seller': 'CableWorx',
                'free_shipping': True,
                'rating': 4.3,
                'review_count': 1250
            },
            {
                'name': 'Portable Power Bank 20000mAh',
                'description': 'High-capacity power bank with dual USB output, LED display, and ultra-fast charging.',
                'price': 1999,
                'discount_price': 1299,
                'category': 'Electronics',
                'stock': 25,
                'seller': 'PowerTech India',
                'free_shipping': True,
                'rating': 4.6,
                'review_count': 856
            },
            {
                'name': 'Smart WiFi Light Bulb',
                'description': 'Smart LED bulb with 16 million colors, voice control, and app compatibility.',
                'price': 1299,
                'discount_price': 799,
                'category': 'Electronics',
                'stock': 30,
                'seller': 'SmartHome Hub',
                'free_shipping': False,
                'rating': 4.2,
                'review_count': 523
            },
            {
                'name': 'Phone Screen Protector 2-Pack',
                'description': 'Tempered glass screen protector with 9H hardness and anti-glare coating.',
                'price': 299,
                'discount_price': 149,
                'category': 'Electronics',
                'stock': 100,
                'seller': 'ScreenGuard Plus',
                'free_shipping': True,
                'rating': 4.4,
                'review_count': 2145
            },

            # Fashion (5 products)
            {
                'name': 'Cotton T-Shirt Pack',
                'description': 'Pack of 3 premium cotton t-shirts, available in multiple colors. Comfortable for daily wear.',
                'price': 999,
                'discount_price': 499,
                'category': 'Fashion',
                'stock': 40,
                'seller': 'Fashion Hub',
                'free_shipping': True,
                'rating': 4.1,
                'review_count': 678
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic blue denim jeans with comfortable fit and durable stitching. Available in all sizes.',
                'price': 1499,
                'discount_price': 999,
                'category': 'Fashion',
                'stock': 35,
                'seller': 'DenimWorld',
                'free_shipping': True,
                'rating': 4.5,
                'review_count': 891
            },
            {
                'name': 'Casual Sneakers',
                'description': 'Lightweight and stylish sneakers perfect for casual outings. Breathable mesh material.',
                'price': 2499,
                'discount_price': 1799,
                'category': 'Fashion',
                'stock': 20,
                'seller': 'ShoeStyle',
                'free_shipping': True,
                'rating': 4.3,
                'review_count': 445
            },
            {
                'name': 'Wool Winter Sweater',
                'description': 'Warm wool sweater ideal for winter. Comfortable and stylish with high-quality knit.',
                'price': 1999,
                'discount_price': 1299,
                'category': 'Fashion',
                'stock': 18,
                'seller': 'WinterWear Co',
                'free_shipping': True,
                'rating': 4.4,
                'review_count': 567
            },
            {
                'name': 'Leather Belt',
                'description': 'Premium genuine leather belt with adjustable fit and elegant buckle design.',
                'price': 899,
                'discount_price': 549,
                'category': 'Fashion',
                'stock': 45,
                'seller': 'LeatherCraft',
                'free_shipping': True,
                'rating': 4.2,
                'review_count': 734
            },

            # Home & Kitchen (5 products)
            {
                'name': 'Stainless Steel Cookware Set',
                'description': '10-piece cookware set with non-stick coating, heat-resistant handles, and oven-safe design.',
                'price': 4999,
                'discount_price': 2999,
                'category': 'Home & Kitchen',
                'stock': 12,
                'seller': 'KitchenPro',
                'free_shipping': True,
                'rating': 4.6,
                'review_count': 312
            },
            {
                'name': 'Electric Kettle 1.5L',
                'description': 'Fast boiling electric kettle with auto shut-off, stainless steel body, and 1500W power.',
                'price': 799,
                'discount_price': 499,
                'category': 'Home & Kitchen',
                'stock': 28,
                'seller': 'ElectroKitch',
                'free_shipping': False,
                'rating': 4.3,
                'review_count': 623
            },
            {
                'name': 'Microfiber Kitchen Towels Set',
                'description': 'Set of 6 highly absorbent microfiber kitchen towels. Quick-drying and versatile.',
                'price': 399,
                'discount_price': 199,
                'category': 'Home & Kitchen',
                'stock': 60,
                'seller': 'HomeEssentials',
                'free_shipping': True,
                'rating': 4.1,
                'review_count': 1456
            },
            {
                'name': 'Bamboo Cutting Board Set',
                'description': 'Set of 3 eco-friendly bamboo cutting boards, naturally antimicrobial and durable.',
                'price': 599,
                'discount_price': 349,
                'category': 'Home & Kitchen',
                'stock': 35,
                'seller': 'EcoKitchen',
                'free_shipping': True,
                'rating': 4.4,
                'review_count': 589
            },
            {
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with touch control, 5 brightness levels, and USB charging port.',
                'price': 1299,
                'discount_price': 799,
                'category': 'Home & Kitchen',
                'stock': 22,
                'seller': 'LightingPlus',
                'free_shipping': True,
                'rating': 4.5,
                'review_count': 401
            },

            # Books (4 products)
            {
                'name': 'The Psychology of Money',
                'description': 'An insightful book on financial behavior and wealth management. Perfect for investors and learners.',
                'price': 499,
                'discount_price': 299,
                'category': 'Books',
                'stock': 50,
                'seller': 'BookStore Prime',
                'free_shipping': True,
                'rating': 4.7,
                'review_count': 1823
            },
            {
                'name': 'Atomic Habits',
                'description': 'Bestselling guide to building good habits and breaking bad ones. Practical and life-changing.',
                'price': 599,
                'discount_price': 399,
                'category': 'Books',
                'stock': 35,
                'seller': 'BookStore Prime',
                'free_shipping': True,
                'rating': 4.8,
                'review_count': 2934
            },
            {
                'name': 'The Alchemist',
                'description': 'A philosophical novel about following your dreams and personal legend. Inspiring and uplifting.',
                'price': 399,
                'discount_price': 249,
                'category': 'Books',
                'stock': 45,
                'seller': 'BookStore Prime',
                'free_shipping': True,
                'rating': 4.6,
                'review_count': 1567
            },
            {
                'name': 'Sapiens',
                'description': 'A sweeping history of humankind from the Stone Age to modern day. Thought-provoking and educational.',
                'price': 799,
                'discount_price': 499,
                'category': 'Books',
                'stock': 28,
                'seller': 'BookStore Prime',
                'free_shipping': True,
                'rating': 4.5,
                'review_count': 1204
            },

            # Sports (1 product to make 20 total)
            {
                'name': 'Yoga Mat Non-Slip',
                'description': 'Premium non-slip yoga mat made from eco-friendly TPE material. 6mm thick for comfort and stability.',
                'price': 1299,
                'discount_price': 799,
                'category': 'Sports',
                'stock': 32,
                'seller': 'FitnessPro',
                'free_shipping': True,
                'rating': 4.4,
                'review_count': 876
            },
        ]

        # Create products
        products_created = 0
        products_skipped = 0

        for product_data in products_data:
            category = categories[product_data.pop('category')]
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={**product_data, 'category': category}
            )
            
            if created:
                products_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {product.name}')
                )
            else:
                products_skipped += 1
                self.stdout.write(f'• Already exists: {product.name}')

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Products Created: {products_created}'))
        self.stdout.write(f'• Products Skipped: {products_skipped}')
        self.stdout.write('='*60)
        self.stdout.write(
            self.style.SUCCESS('\n✅ Sample data loaded successfully!')
        )
        self.stdout.write('Visit http://127.0.0.1:8000/ to browse products\n')
