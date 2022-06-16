import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from reviews.models import GenreTitle
        with open(r'static\data\genre_title.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                genre_title = GenreTitle(
                    id=row[0], title_id=row[1], genre_id=row[2]
                )
                genre_title.save()
