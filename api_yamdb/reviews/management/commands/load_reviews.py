import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def load_reviews(self):
        from reviews.models import Review
        with open(r'static\data\review.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                review = Review(
                    id=row[0], title_id=row[1],
                    text=row[2], author_id=row[3],
                    score=row[4], pub_date=row[5]
                )
                review.save()

    def handle(self, *args, **options):
        self.load_reviews()
