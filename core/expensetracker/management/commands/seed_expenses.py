from datetime import timedelta
from decimal import Decimal
import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from expensetracker.models import Category, Expense, User


class Command(BaseCommand):
    help = "Seed the database with categories and expenses for existing users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default=None,
            help="Seed only this username. If omitted, all users are seeded.",
        )
        parser.add_argument(
            "--categories-per-user",
            type=int,
            default=5,
            help="How many categories to ensure for each user (default: 5).",
        )
        parser.add_argument(
            "--expenses-per-user",
            type=int,
            default=1200,
            help="How many expense rows to create per user (default: 1200).",
        )
        parser.add_argument(
            "--days-back",
            type=int,
            default=365,
            help="Spread generated expense dates over this many days (default: 365).",
        )

    def handle(self, *args, **options):
        username = options["username"]
        categories_per_user = options["categories_per_user"]
        expenses_per_user = options["expenses_per_user"]
        days_back = options["days_back"]

        if categories_per_user < 1:
            raise CommandError("--categories-per-user must be at least 1")
        if expenses_per_user < 1:
            raise CommandError("--expenses-per-user must be at least 1")
        if days_back < 1:
            raise CommandError("--days-back must be at least 1")

        if username:
            users = list(User.objects.filter(username=username))
            if not users:
                raise CommandError(f"User '{username}' not found.")
        else:
            users = list(User.objects.all())
        if not users:
            raise CommandError("No users found. Create at least one user first.")

        now = timezone.localdate()
        category_prefixes = [
            "Food",
            "Transport",
            "Bills",
            "Shopping",
            "Health",
            "Entertainment",
            "Education",
            "Travel",
            "Groceries",
            "Utilities",
        ]
        description_pool = [
            "Monthly recurring payment",
            "Quick purchase",
            "Team lunch",
            "Personal expense",
            "Home related",
            "Online order",
            "Transportation fare",
            "Medical cost",
            "Weekend activity",
            "Daily essentials",
        ]

        created_categories = 0
        created_expenses = 0

        # A fixed seed keeps generated data reproducible between runs.
        random.seed(42)

        with transaction.atomic():
            for user in users:
                user_categories = list(
                    Category.objects.filter(user=user).order_by("id")
                )

                needed = max(0, categories_per_user - len(user_categories))
                start_idx = len(user_categories)
                for i in range(needed):
                    base_name = category_prefixes[(start_idx + i) % len(category_prefixes)]
                    unique_name = f"{base_name}-{start_idx + i + 1}"
                    category = Category.objects.create(
                        user=user,
                        name=unique_name,
                        description=f"Auto-generated category {unique_name}",
                    )
                    user_categories.append(category)
                    created_categories += 1

                expense_batch = []
                for _ in range(expenses_per_user):
                    random_days = random.randint(0, days_back - 1)
                    amount = Decimal(str(round(random.uniform(2.5, 2500.0), 2)))
                    chosen_category = random.choice(user_categories)
                    expense_batch.append(
                        Expense(
                            user=user,
                            category=chosen_category,
                            amount=amount,
                            description=chosen_category.description or random.choice(description_pool),
                            date=now - timedelta(days=random_days),
                        )
                    )

                Expense.objects.bulk_create(expense_batch, batch_size=1000)
                created_expenses += len(expense_batch)

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
        self.stdout.write(
            f"Users processed: {len(users)} | Categories created: {created_categories} | "
            f"Expenses created: {created_expenses}"
        )
