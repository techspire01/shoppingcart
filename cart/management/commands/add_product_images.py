import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from cart.models import Product


class Command(BaseCommand):
    help = 'Add placeholder images to all products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        total = products.count()
        updated = 0

        # Category-based image mapping for variety
        category_images = {
            'Electronics': {
                'primary': [1, 2, 3, 4, 5],
                'secondary': [10, 11, 12, 13, 14]
            },
            'Fashion': {
                'primary': [20, 21, 22, 23, 24],
                'secondary': [25, 26, 27, 28, 29]
            },
            'Home & Kitchen': {
                'primary': [30, 31, 32, 33, 34],
                'secondary': [35, 36, 37, 38, 39]
            },
            'Books': {
                'primary': [40, 41, 42, 43],
                'secondary': [44, 45, 46, 47]
            },
            'Sports': {
                'primary': [50],
                'secondary': [51, 52, 53, 54]
            }
        }

        for idx, product in enumerate(products, 1):
            try:
                # Get image IDs for this category
                category_name = product.category.name
                if category_name in category_images:
                    image_ids = category_images[category_name]['primary']
                    secondary_ids = category_images[category_name]['secondary']
                else:
                    image_ids = list(range(1, 20))
                    secondary_ids = list(range(20, 40))

                # Rotate through available images
                primary_idx = idx % len(image_ids)
                secondary_idx = (idx + len(image_ids)) % len(secondary_ids)

                primary_id = image_ids[primary_idx]
                secondary_id = secondary_ids[secondary_idx]

                # Download and save primary image
                if not product.image:
                    try:
                        img_url = f'https://picsum.photos/400/400?random={primary_id}'
                        response = requests.get(img_url, timeout=10)
                        if response.status_code == 200:
                            filename = f'{product.id}_main.jpg'
                            product.image.save(
                                filename,
                                ContentFile(response.content),
                                save=False
                            )
                            self.stdout.write(f'  ✓ Main image: {product.name}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Main image failed: {product.name} - {str(e)}')
                        )

                # Download and save secondary images
                for field_num in [2, 3, 4]:
                    field_name = f'image{field_num}'
                    if not getattr(product, field_name):
                        try:
                            img_seed = primary_id + field_num
                            img_url = f'https://picsum.photos/400/400?random={img_seed}'
                            response = requests.get(img_url, timeout=10)
                            if response.status_code == 200:
                                filename = f'{product.id}_img{field_num}.jpg'
                                getattr(product, field_name).save(
                                    filename,
                                    ContentFile(response.content),
                                    save=False
                                )
                                self.stdout.write(f'  ✓ Image {field_num}: {product.name}')
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(f'  ⚠ Image {field_num} failed: {product.name}')
                            )

                # Save product with all images
                product.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'[{idx}/{total}] ✓ {product.name}'))

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[{idx}/{total}] ✗ {product.name}: {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Products Updated: {updated}/{total}'))
        self.stdout.write('='*60 + '\n')
        self.stdout.write(self.style.SUCCESS('✅ Product images added successfully!'))
        self.stdout.write('Images are downloaded from picsum.photos\n')
