from django.contrib import admin
from .models import Pferd, Fuetterung, ZugangHistorie

admin.site.register(Pferd)
admin.site.register(Fuetterung)
admin.site.register(ZugangHistorie)

