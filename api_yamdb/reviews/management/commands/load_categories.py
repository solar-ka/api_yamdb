import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from reviews.models import Category
        with open(r'static\data\category.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                category = Category(id=row[0], name=row[1], slug=row[2],)
                category.save()
