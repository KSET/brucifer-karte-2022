from django.db import models


class Role(models.TextChoices):
    NONE = "none", "Ništa"
    ADMIN = "admin", "Admin"
    ENTRY = "entry", "Ulaz"
    TICKETS = "tickets", "Karte"
    ENTRY_TICKETS = "entry_tickets", "Ulaz+Karte"


# Admin is listed explicitly; roles have no implicit hierarchy.
GUEST_ROLES = (Role.ENTRY, Role.TICKETS, Role.ENTRY_TICKETS, Role.ADMIN)
MANAGE_ROLES = (Role.ADMIN,)
