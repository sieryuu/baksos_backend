from django.contrib import admin

from referensi.models import Penyakit, Puskesmas

# Register your models here.
admin.site.register(Puskesmas)
admin.site.register(Penyakit)
