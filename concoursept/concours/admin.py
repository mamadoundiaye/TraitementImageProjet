from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from admin_interface.models import Theme  # pour unregister(Theme)

# Register your models here.
from .models import *


class CandidatA(admin.ModelAdmin):
    # exclude = ('date_de_naissance', )
    list_display = ("candidat_id", "prenom", "nom", "lycee", "centre", "moy_general")
    list_filter = ("centre", "lycee")

    readonly_fields = (
        "prenom",
        "nom",
        "lycee",
        "centre",
        "mail",
        "telephone",
        "genie",
        "moy_general",
        "moy_seconde",
        "moy_premiere",
        "moy_terminale",
        "moy_bac",
    )
    list_per_page = 20


admin.site.register(Candidat, CandidatA)

# unregister Group , User , Theme
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Theme)

# PERSONNALISATION
admin.site.site_header = "CONCOURS EPT ADMINISTRATION"
admin.site.site_title = "CONCOURS EPT administration"
admin.site.index_title = "Site d'administration du concours d'entree a l'EPT"
admin.site.empty_value_display = "*"
