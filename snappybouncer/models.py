from django.db import models
from django.db.models import DateTimeField
from django.utils import timezone

from snappybouncer.tasks import create_snappy_ticket


# Modelled on https://github.com/jamesmarlowe/django-AutoDateTimeFields
# But with timezone support
class AutoDateTimeField(DateTimeField):
    def pre_save(self, model_instance, add):
        now = timezone.now()
        setattr(model_instance, self.attname, now)
        return now


class AutoNewDateTimeField(DateTimeField):
    def pre_save(self, model_instance, add):
        if not add:
            return getattr(model_instance, self.attname)
        now = timezone.now()
        setattr(model_instance, self.attname, now)
        return now


class UserAccount(models.Model):
    """ Vumi User Accounts that can send data
    """
    key = models.CharField(max_length=43)
    name = models.CharField(max_length=200)
    notes = models.TextField(verbose_name=u'Notes', null=True, blank=True)
    created_at = AutoNewDateTimeField(blank=True)
    updated_at = AutoDateTimeField(blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Conversation(models.Model):
    """ A conversation that can deliver messages into system
    """
    user_account = models.ForeignKey(
        UserAccount, related_name='conversations', null=False)
    key = models.CharField(max_length=43)
    name = models.CharField(max_length=200)
    notes = models.TextField(verbose_name=u'Notes', null=True, blank=True)
    created_at = AutoNewDateTimeField(blank=True)
    updated_at = AutoDateTimeField(blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Ticket(models.Model):
    """ Support tickets
    """
    conversation = models.ForeignKey(
        Conversation, related_name='tickets', null=False)
    support_nonce = models.CharField(max_length=43, null=True, blank=True)
    support_id = models.IntegerField(null=True, blank=True)
    message = models.TextField(
        verbose_name=u'Inbound Message', null=False, blank=False)
    response = models.TextField(
        verbose_name=u'Outbound Response', null=True, blank=True)
    contact_key = models.CharField(max_length=43)
    msisdn = models.CharField(max_length=100)
    created_at = AutoNewDateTimeField(blank=True)
    updated_at = AutoDateTimeField(blank=True)

    def __unicode__(self):
        return "%s" % self.message


# Make sure new tickets are sent to Snappy via Celery
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Ticket)
def fire_snappy_if_new(sender, instance, created, **kwargs):
    if created:
        create_snappy_ticket.delay(instance)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], [
    "^snappybouncer\.models\.AutoNewDateTimeField",
    "^snappybouncer\.models\.AutoDateTimeField"])
