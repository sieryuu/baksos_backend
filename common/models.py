from datetime import date, datetime
from typing import Iterable, Optional
from django.db import models
from crum import get_current_user

# Create your models here.

class CrudModelManager(models.Manager):
    def bulk_create(self, objs, batch_size=1000, ignore_conflicts=False):
        current_user = get_current_user().username
        for obj in objs:
            obj.dibuat_oleh = current_user
            obj.waktu_dibuat = datetime.now()
            obj.diperbaharui_oleh = current_user
            obj.waktu_diperbaharui = datetime.now()
        return super().bulk_create(objs, batch_size, ignore_conflicts)
    
        
class CrudModel(models.Model):
    dibuat_oleh = models.CharField(max_length=50)
    waktu_dibuat = models.DateTimeField(auto_created=True)
    diperbaharui_oleh = models.CharField(max_length=50)
    waktu_diperbaharui = models.DateTimeField(auto_now=True)

    objects: CrudModelManager()
    
    class Meta:
        abstract = True

    def save(self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = "default",
        update_fields: Optional[Iterable[str]] = None,) -> None:
        current_user = get_current_user().username
        self.dibuat_oleh = current_user
        self.diperbaharui_oleh = current_user
        return super().save(force_insert, force_update, using, update_fields)