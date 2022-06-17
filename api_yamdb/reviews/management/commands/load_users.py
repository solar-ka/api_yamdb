import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def load_users(self):
        from reviews.models import User
        with open(r'static\data\users.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                user = User(
                    id=row[0], username=row[1],
                    email=row[2], role=row[3], bio=row[4],
                    first_name=row[5], last_name=row[6])
                user.save()

    def handle(self, *args, **options):
        self.load_users()
