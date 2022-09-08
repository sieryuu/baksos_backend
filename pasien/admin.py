from django.contrib import admin

from pasien.models import DetailPasien, Pasien, ScreeningPasien

# Register your models here.
admin.site.register(Pasien)
admin.site.register(DetailPasien)
admin.site.register(ScreeningPasien)

