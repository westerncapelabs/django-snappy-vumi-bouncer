from django.contrib import admin
from snappybouncer.models import Conversation, UserAccount, Ticket
from snappybouncer.actions import export_select_fields_csv_action


class TicketAdmin(admin.ModelAdmin):
    actions = [export_select_fields_csv_action(
        "Export selected objects as CSV file",
        fields=[
            ("id", "unique_id"),
            ("support_nonce", "support_nonce"),
            ("message", "Message"),
            ("response", "Response"),
            ("created_at", "Created At"),
            ("updated_at", "Updated At"),
        ],
        header=True
        )]


admin.site.register(Conversation)
admin.site.register(UserAccount)
admin.site.register(Ticket, TicketAdmin)
