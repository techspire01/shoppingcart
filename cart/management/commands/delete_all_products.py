from django.core.management.base import BaseCommand
from cart.models import Product, CartItem, OrderItem, WishlistItem, ProductReview


class Command(BaseCommand):
    help = 'Delete all products from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompt',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            confirm = input('⚠️  This will DELETE ALL PRODUCTS from the database! Are you sure? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('❌ Deletion cancelled'))
                return

        # Count before deletion
        total_products = Product.objects.count()
        total_cart_items = CartItem.objects.count()
        total_order_items = OrderItem.objects.count()
        total_wishlist_items = WishlistItem.objects.count()
        total_reviews = ProductReview.objects.count()

        self.stdout.write(f'\nDeleting...')
        self.stdout.write(f'  • CartItems: {total_cart_items}')
        self.stdout.write(f'  • OrderItems: {total_order_items}')
        self.stdout.write(f'  • WishlistItems: {total_wishlist_items}')
        self.stdout.write(f'  • ProductReviews: {total_reviews}')
        self.stdout.write(f'  • Products: {total_products}\n')

        # Delete related items first
        CartItem.objects.all().delete()
        OrderItem.objects.all().delete()
        WishlistItem.objects.all().delete()
        ProductReview.objects.all().delete()
        
        # Delete products
        Product.objects.all().delete()

        # Verify deletion
        remaining = Product.objects.count()
        
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('✅ All products deleted successfully!'))
        self.stdout.write(f'Remaining products: {remaining}')
        self.stdout.write('='*60 + '\n')
