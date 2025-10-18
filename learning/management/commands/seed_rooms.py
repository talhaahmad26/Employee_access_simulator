from django.core.management.base import BaseCommand
from learning.models import Room
import datetime

class Command(BaseCommand):
    help = "Seed rooms per assessment rules"

    def handle(self, *args, **options):
        data = [
            {"name":"ServerRoom", "min_access_level":2, "open_time":"09:00", "close_time":"11:00", "cooldown_minutes":15},
            {"name":"Vault", "min_access_level":3, "open_time":"09:00", "close_time":"10:00", "cooldown_minutes":30},
            {"name":"R&D Lab", "min_access_level":1, "open_time":"08:00", "close_time":"12:00", "cooldown_minutes":10},
        ]
        for d in data:
            h,m = map(int, d["open_time"].split(":"))
            ch,cm = map(int, d["close_time"].split(":"))
            obj, created = Room.objects.update_or_create(
                name=d["name"],
                defaults={
                    "min_access_level": d["min_access_level"],
                    "open_time": datetime.time(h,m),
                    "close_time": datetime.time(ch,cm),
                    "cooldown_minutes": d["cooldown_minutes"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated {obj.name}"))
        self.stdout.write(self.style.SUCCESS("Seeding complete."))