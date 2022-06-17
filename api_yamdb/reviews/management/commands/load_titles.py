import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def load_titles(self):
        from reviews.models import Title
        with open(r'static\data\titles.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                title = Title(
                    id=row[0], name=row[1],
                    year=row[2], category_id=row[3]
                )
                title.save()

    def handle(self, *args, **options):
        self.load_titles()
