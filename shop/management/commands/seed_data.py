from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with sample categories and products."

    def handle(self, *args, **options):
        categories = ['Fiction', 'Non-Fiction', 'Academic', 'Comics']
        cat_objs = {}
        for name in categories:
            cat, _ = Category.objects.get_or_create(name=name)
            cat_objs[name] = cat

        products = [
            dict(name='The Silent Ocean', category='Fiction', price=450,
                 description='A gripping novel about a fisherman lost at sea and the family waiting for his return.',
                 quantity=25, is_featured=True),
            dict(name='Modern Physics Simplified', category='Academic', price=650,
                 description='An accessible introduction to modern physics concepts for undergraduate students.',
                 quantity=15, is_featured=True),
            dict(name='The Art of Slow Living', category='Non-Fiction', price=380,
                 description='Practical wisdom on mindfulness, minimalism, and living intentionally.',
                 quantity=30, is_featured=True),
            dict(name='Shadow Realm Vol. 1', category='Comics', price=290,
                 description='The first volume in an action-packed graphic novel series set in a fantasy realm.',
                 quantity=20, is_featured=True),
            dict(name='Whispers of the Forest', category='Fiction', price=420,
                 description='A coming-of-age story set in a small village on the edge of an ancient forest.',
                 quantity=18, is_featured=False),
            dict(name='Introduction to Economics', category='Academic', price=550,
                 description='A clear, example-driven textbook covering the fundamentals of micro and macroeconomics.',
                 quantity=12, is_featured=False),
            dict(name='Cooking with Heart', category='Non-Fiction', price=320,
                 description='A collection of comforting home-style recipes from around the world.',
                 quantity=22, is_featured=False),
            dict(name='Shadow Realm Vol. 2', category='Comics', price=290,
                 description='The story continues as new heroes rise to face the growing darkness.',
                 quantity=0, is_featured=False),
        ]

        for p in products:
            Product.objects.get_or_create(
                name=p['name'],
                defaults=dict(
                    category=cat_objs[p['category']],
                    price=p['price'],
                    description=p['description'],
                    quantity=p['quantity'],
                    is_featured=p['is_featured'],
                )
            )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully.'))
