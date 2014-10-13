import logging
import json
import re
import urlparse
from HTMLParser import HTMLParser

from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource, Resource, ALL, Bundle
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer

from snappybouncer.models import Conversation, UserAccount, Ticket
from snappybouncer.tasks import send_helpdesk_response

logger = logging.getLogger(__name__)

# ModelResource access using standard format


class UserAccountResource(ModelResource):

    class Meta:
        queryset = UserAccount.objects.all()
        resource_name = 'useraccount'
        list_allowed_methods = ['get']
        include_resource_uri = True
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        filtering = {
            'key': ALL,
        }


class ConversationResource(ModelResource):
    user_account = fields.ToOneField(UserAccountResource, 'user_account')

    class Meta:
        queryset = Conversation.objects.all()
        resource_name = 'conversation'
        list_allowed_methods = ['get']
        include_resource_uri = True
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        filtering = {
            'key': ALL,
            'user_account': ALL
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/key/(?P<key>[\w\d_.-]+)/$" %
                self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class TicketResource(ModelResource):
    conversation = fields.ToOneField(ConversationResource, 'conversation')

    class Meta:
        queryset = Ticket.objects.all()
        resource_name = 'ticket'
        list_allowed_methods = ['get', 'post']
        include_resource_uri = True
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        filtering = {
            'contact_key': ALL,
            'msisdn': ALL,
            'user_account': ALL
        }


# Resource custom API for WebHooks

class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
    }

    def from_urlencode(self, data, options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v) > 1 else v[0])
                  for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self, content):
        pass


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# We need a generic object to shove data in/get data from.


class WebhookObject(object):

    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class WebhookResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    event = fields.CharField(attribute='event')
    data = fields.CharField(attribute='data')

    class Meta:
        resource_name = 'listener'
        list_allowed_methods = ['post']
        object_class = WebhookObject
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = urlencodeSerializer()

    # The following methods need overriding regardless of the
    # data source.
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    def obj_create(self, bundle, **kwargs):
        bundle.obj = WebhookObject(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        # React to the specific events
        allowed_events = ['message.outgoing']
        if bundle.obj.event in allowed_events:
            # strips newlines from dodgy json from API - bug logged
            # and turns into a dict
            bundle.obj.data = json.loads(re.sub("\\n", "", bundle.obj.data))
            if bundle.obj.event == 'message.outgoing':
                # Get the pre-existing ticket
                ticket = Ticket.objects.get(
                    support_nonce=bundle.obj.data["note"]["ticket"]["nonce"])
                try:
                    ticket.response = strip_tags(
                        bundle.obj.data["note"]["content"])
                    ticket.support_id = int(
                        bundle.obj.data["note"]["ticket"]["id"])
                    ticket.save()
                    # Send the message out to user via Vumi via Celery
                    send_helpdesk_response.delay(ticket)
                except ObjectDoesNotExist:
                    logger.error(
                        'Webhook received for unrecognised support ticket',
                        exc_info=True)
        return bundle
