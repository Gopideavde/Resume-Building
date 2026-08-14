from django.db import migrations
from datetime import timedelta

def backfill_expiry_date(apps, schema_editor):
    PremiumAccess = apps.get_model('payments', 'PremiumAccess')
    for access in PremiumAccess.objects.filter(expiry_date__isnull=True):
        access.expiry_date = access.granted_at + timedelta(days=30)
        access.save()

class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_premiumaccess_expiry_date'),
    ]

    operations = [
        migrations.RunPython(backfill_expiry_date),
    ]
