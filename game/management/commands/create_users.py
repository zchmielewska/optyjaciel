from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker


faker = Faker("pl_PL")


class Command(BaseCommand):
    help = "Populate db with fake users"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        for _ in range(options["count"]):
            username = faker.profile()["username"]
            password = faker.password()
            User.objects.create_user(username=username, password=password)
