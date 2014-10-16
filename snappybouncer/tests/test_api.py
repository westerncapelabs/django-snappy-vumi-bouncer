"""
Tests for Snappy Bouncer.
"""

import json

from django.contrib.auth.models import User
from django.core import management
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey

from snappybouncer.models import Conversation, UserAccount, Ticket

from .helpers import PostSaveHelper


class SnappyBouncerResourceTest(ResourceTestCase):

    def setUp(self):
        super(SnappyBouncerResourceTest, self).setUp()
        self._post_save_helper = PostSaveHelper()
        self._post_save_helper.replace()
        management.call_command(
            'loaddata', 'test_snappybouncer.json', verbosity=0)

        # Create a user.
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(
            self.username, 'testuser@example.com', self.password)
        ApiKey.objects.create(user=self.user)
        self.api_key = self.user.api_key.key

    def tearDown(self):
        self._post_save_helper.restore()

    def get_credentials(self):
        return self.create_apikey(self.username, self.api_key)

    def test_data_loaded(self):
        useraccounts = UserAccount.objects.all()
        self.assertEqual(useraccounts.count(), 1)
        conversations = Conversation.objects.all()
        self.assertEqual(conversations.count(), 1)

        tickets = Ticket.objects.all()
        self.assertEqual(tickets.count(), 3)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get(
            '/api/v1/snappybouncer/useraccount/', format='json'))

    def test_api_keys_created(self):
        self.assertEqual(True, self.api_key is not None)

    def test_get_useraccount_list_json(self):
        resp = self.api_client.get(
            '/api/v1/snappybouncer/useraccount/', format='json',
            authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)

    def test_get_useraccount_filtered_list_json(self):
        filter_data = {
            "key": "useraccountkey"
        }

        resp = self.api_client.get(
            '/api/v1/snappybouncer/useraccount/', data=filter_data,
            format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)

    def test_get_useraccount_filtered_list_denied_json(self):
        filter_data = {
            "name": "useraccountkey"
        }

        resp = self.api_client.get(
            '/api/v1/snappybouncer/useraccount/', data=filter_data,
            format='json', authentication=self.get_credentials())
        json_item = json.loads(resp.content)
        self.assertHttpBadRequest(resp)
        self.assertEqual(
            "The 'name' field does not allow filtering.", json_item["error"])

    def test_post_ticket_good(self):
        data = {
            "contact_key": "dummycontactkey2",
            "conversation": "/api/v1/snappybouncer/conversation/1/",
            "msisdn": "+271234",
            "message": "New item to send to snappy"
        }

        response = self.api_client.post(
            '/api/v1/snappybouncer/ticket/', format='json',
            authentication=self.get_credentials(), data=data)
        json_item = json.loads(response.content)
        self.assertEqual("dummycontactkey2", json_item["contact_key"])
        self.assertEqual(
            "/api/v1/snappybouncer/conversation/1/", json_item["conversation"])
        self.assertEqual("+271234", json_item["msisdn"])
        self.assertEqual(
            "/api/v1/snappybouncer/ticket/4/", json_item["resource_uri"])

    def test_post_ticket_bad_conversation(self):
        data = {
            "contact_key": "dummycontactkey2",
            "conversation": "/api/v1/snappybouncer/conversation/2/",
            "msisdn": "+271234",
            "message": "New item to send to snappy"
        }

        response = self.api_client.post(
            '/api/v1/snappybouncer/ticket/', format='json',
            authentication=self.get_credentials(), data=data)
        self.assertHttpBadRequest(response)
