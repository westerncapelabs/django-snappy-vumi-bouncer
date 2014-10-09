from django.contrib import admin
from snappybouncer.models import Conversation, UserAccount, Ticket

admin.site.register(Conversation)
admin.site.register(UserAccount)
admin.site.register(Ticket)
