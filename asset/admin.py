from django.contrib import admin
from models import AssetCategory, User, UsageStatus, DiscardStatus

# Register your models here.

admin.site.register([AssetCategory, UsageStatus, DiscardStatus])
