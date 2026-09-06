from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from management_utils.models import Profile
import os


class Command(BaseCommand):
    help = (
        "Create the initial UNIBEN IEPRTS administrator from Render environment "
        "variables. Safe to run repeatedly; an existing username is left unchanged."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Admin setup skipped: set DJANGO_SUPERUSER_USERNAME, "
                    "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD in "
                    "the Render environment, then redeploy."
                )
            )
            return

        User = get_user_model()

        with transaction.atomic():
            user = User.objects.filter(username=username).first()

            if user is None:
                user = User(
                    username=username,
                    email=email,
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                )
                user.set_password(password)
                user.save()
                created = True
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Administrator '{username}' created successfully."
                    )
                )
            else:
                created = False
                self.stdout.write(
                    self.style.WARNING(
                        f"Administrator '{username}' already exists; "
                        "no password or account details were changed."
                    )
                )

            # Ensure the IEPRTS profile exists and has administrator role.
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": "admin"},
            )
            if profile.role != "admin":
                profile.role = "admin"
                profile.save(update_fields=["role"])

            if profile_created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"IEPRTS administrator profile created for '{username}'."
                    )
                )

            if not created:
                self.stdout.write(
                    self.style.NOTICE(
                        "If you need to change the administrator password, use "
                        "Django admin or run the command locally with a deliberate "
                        "password change; this deployment command never overwrites "
                        "an existing administrator password."
                    )
                )
