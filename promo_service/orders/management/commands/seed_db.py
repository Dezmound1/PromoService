from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from goods.models import Good
from users.models import User
from promocode.models import DiscountPromoCode


class Command(BaseCommand):
    help = "Seed database with mock data for goods, users, and promocodes (not orders)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="You'll delete all data from db before seeding new data. Use with caution!",
        )

    def handle(self, *args, **options):

        if options["clear"]:
            self.stdout.write("Clearing data")
            DiscountPromoCode.objects.all().delete()
            Good.objects.all().delete()
            User.objects.all().delete()
            self.stdout.write("Data cleared!")

        self._create_users()
        self._create_goods()
        self._create_promocodes()

        self.stdout.write("All processes done!")

    def _create_users(self):
        users = [
            {
                "username": "ivan_petrov",
                "email": "ivan@example.com",
                "password": "hashed_pass_1",
            },
            {
                "username": "anna_smirnova",
                "email": "anna@example.com",
                "password": "hashed_pass_2",
            },
            {
                "username": "dmitry_kozlov",
                "email": "dmitry@example.com",
                "password": "hashed_pass_3",
            },
            {
                "username": "elena_volkova",
                "email": "elena@example.com",
                "password": "hashed_pass_4",
            },
            {
                "username": "sergey_novikov",
                "email": "sergey@example.com",
                "password": "hashed_pass_5",
            },
        ]
        for data in users:
            User.objects.get_or_create(
                username=data["username"],
                defaults=data,
            )

    def _create_goods(self):
        goods = [
            {
                "name": "Cyberpunk 2077",
                "price": Decimal("2499.99"),
                "count": 50,
                "category": Good.Status.GAME,
                "promo_eligible": True,
            },
            {
                "name": "The Witcher 3",
                "price": Decimal("999.99"),
                "count": 100,
                "category": Good.Status.GAME,
                "promo_eligible": True,
            },
            {
                "name": "CS2 AK-47 Neon Rider",
                "price": Decimal("3500.00"),
                "count": 10,
                "category": Good.Status.SKIN,
                "promo_eligible": True,
            },
            {
                "name": "Dota 2 Arcana Pudge",
                "price": Decimal("1800.00"),
                "count": 25,
                "category": Good.Status.SKIN,
                "promo_eligible": False,
            },
            {
                "name": "NordVPN 1 Year",
                "price": Decimal("4990.00"),
                "count": 200,
                "category": Good.Status.VPN,
                "promo_eligible": True,
            },
            {
                "name": "ExpressVPN 6 Months",
                "price": Decimal("2990.00"),
                "count": 150,
                "category": Good.Status.VPN,
                "promo_eligible": True,
            },
            {
                "name": "Spotify Premium 1 Month",
                "price": Decimal("299.00"),
                "count": 500,
                "category": Good.Status.SUBSCRIPTION,
                "promo_eligible": True,
            },
            {
                "name": "YouTube Premium 1 Month",
                "price": Decimal("399.00"),
                "count": 500,
                "category": Good.Status.SUBSCRIPTION,
                "promo_eligible": False,
            },
            {
                "name": "Steam Gift Card 1000₽",
                "price": Decimal("1000.00"),
                "count": 300,
                "category": Good.Status.ANOTHER,
                "promo_eligible": False,
            },
            {
                "name": "PlayStation Plus 3 Months",
                "price": Decimal("1799.00"),
                "count": 80,
                "category": Good.Status.SUBSCRIPTION,
                "promo_eligible": True,
            },
        ]
        for data in goods:
            Good.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )

    def _create_promocodes(self):
        now = timezone.now()
        promocodes = [
            {
                "code": "WELCOME10",
                "is_active": True,
                "valid_until": now + timedelta(days=30),
                "max_usages": 100,
                "discount_percent": 10,
                "allowed_category": None,
            },
            {
                "code": "GAME25",
                "is_active": True,
                "valid_until": now + timedelta(days=14),
                "max_usages": 50,
                "discount_percent": 25,
                "allowed_category": Good.Status.GAME,
            },
            {
                "code": "SKIN15",
                "is_active": True,
                "valid_until": now + timedelta(days=7),
                "max_usages": 30,
                "discount_percent": 15,
                "allowed_category": Good.Status.SKIN,
            },
            {
                "code": "VPN50",
                "is_active": True,
                "valid_until": now + timedelta(days=3),
                "max_usages": 10,
                "discount_percent": 50,
                "allowed_category": Good.Status.VPN,
            },
            {
                "code": "EXPIRED5",
                "is_active": False,
                "valid_until": now - timedelta(days=5),
                "max_usages": 1,
                "discount_percent": 5,
                "allowed_category": None,
            },
        ]
        for data in promocodes:
            DiscountPromoCode.objects.get_or_create(
                code=data["code"],
                defaults=data,
            )
        self.stdout.write(f"Promocodes created: {len(promocodes)}")
