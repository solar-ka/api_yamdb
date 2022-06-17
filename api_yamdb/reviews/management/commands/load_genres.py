import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def load_genres(self):
        from reviews.models import Genre
        with open(r'static\data\genre.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                genre = Genre(id=row[0], name=row[1], slug=row[2],)
                genre.save()

    def handle(self, *args, **options):
        self.load_genres()
