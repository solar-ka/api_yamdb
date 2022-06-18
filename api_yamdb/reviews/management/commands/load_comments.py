import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def load_comments(self):
        from reviews.models import Comment
        with open(r'static\data\comments.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                comment = Comment(
                    id=row[0], review_id=row[1],
                    text=row[2], author_id=row[3], pub_date=row[4]
                )
                comment.save()

    def handle(self, *args, **options):
        self.load_comments()
