from celery import task
from celery.utils.log import get_task_logger

from go_http.send import HttpApiSender
from go_http.contacts import ContactsApiClient
from besnappy import SnappyApiSender

from django.conf import settings

logger = get_task_logger(__name__)


@task()
def send_helpdesk_response(ticket):
    # Make a session to Vumi
    sender = HttpApiSender(
        account_key=settings.VUMI_GO_ACCOUNT_KEY,
        conversation_key=settings.VUMI_GO_CONVERSATION_KEY,
        conversation_token=settings.VUMI_GO_CONVERSATION_TOKEN)
    # Send message
    response = sender.send_text(ticket.msisdn, ticket.response)
    # TODO: Log outbound send metric
    return response


@task()
def create_snappy_ticket(ticket):
    # Make a session to Snappy
    snappy_api = SnappyApiSender(
        api_key=settings.SNAPPY_API_KEY,
        api_url=settings.SNAPPY_BASE_URL
    )
    # Send message
    subject = "Support for %s" % (ticket.msisdn)
    snappy_ticket = snappy_api.create_note(
        mailbox_id=settings.SNAPPY_MAILBOX_ID,
        subject=subject,
        message=ticket.message,
        to_addr=None,
        from_addr=[{"name": ticket.msisdn, "address": settings.SNAPPY_EMAIL}]
    )
    ticket.support_nonce = snappy_ticket
    ticket.save()
    update_snappy_ticket_with_extras.delay(snappy_api, ticket.support_nonce,
                                           ticket.contact_key, subject)
    # TODO: Log ticket created metric
    return True


@task()
def update_snappy_ticket_with_extras(snappy_api, nonce, contact_key, subject):
    # Short-circuit if there are no extras
    if not settings.SNAPPY_EXTRAS:
        return True
    # Gets more extras from Vumi and creates a private note with them
    contacts_api = ContactsApiClient(auth_token=settings.VUMI_GO_API_TOKEN)
    contact = contacts_api.get_contact(contact_key)
    extra_info = ""
    for extra in settings.SNAPPY_EXTRAS:
        extra_info += extra + ": " + contact["extra"][extra] + "\n"
    if extra_info != "":
        # Send private note
        to_addr = [{
            "name": "Internal Information",
            "address": settings.SNAPPY_EMAIL,
        }]
        snappy_api.create_note(
            mailbox_id=settings.SNAPPY_MAILBOX_ID,
            subject=subject,
            message=extra_info,
            to_addr=to_addr,
            id=nonce,
            scope="private",
            staff_id=settings.SNAPPY_STAFF_ID
        )
    return True
