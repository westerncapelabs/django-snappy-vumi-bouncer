# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("tastypie", "0002_add_apikey_index"),
    )

    def forwards(self, orm):
        # Adding model 'UserAccount'
        db.create_table(u'snappybouncer_useraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=43)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('snappybouncer.models.AutoNewDateTimeField')(blank=True)),
            ('updated_at', self.gf('snappybouncer.models.AutoDateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'snappybouncer', ['UserAccount'])

        # Adding model 'Conversation'
        db.create_table(u'snappybouncer_conversation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='conversations', to=orm['snappybouncer.UserAccount'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=43)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('snappybouncer.models.AutoNewDateTimeField')(blank=True)),
            ('updated_at', self.gf('snappybouncer.models.AutoDateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'snappybouncer', ['Conversation'])

        # Adding model 'Ticket'
        db.create_table(u'snappybouncer_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tickets', to=orm['snappybouncer.Conversation'])),
            ('support_nonce', self.gf('django.db.models.fields.CharField')(max_length=43, null=True, blank=True)),
            ('support_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contact_key', self.gf('django.db.models.fields.CharField')(max_length=43)),
            ('msisdn', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('snappybouncer.models.AutoNewDateTimeField')(blank=True)),
            ('updated_at', self.gf('snappybouncer.models.AutoDateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'snappybouncer', ['Ticket'])


    def backwards(self, orm):
        # Deleting model 'UserAccount'
        db.delete_table(u'snappybouncer_useraccount')

        # Deleting model 'Conversation'
        db.delete_table(u'snappybouncer_conversation')

        # Deleting model 'Ticket'
        db.delete_table(u'snappybouncer_ticket')


    models = {
        u'snappybouncer.conversation': {
            'Meta': {'object_name': 'Conversation'},
            'created_at': ('snappybouncer.models.AutoNewDateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('snappybouncer.models.AutoDateTimeField', [], {'blank': 'True'}),
            'user_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conversations'", 'to': u"orm['snappybouncer.UserAccount']"})
        },
        u'snappybouncer.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'contact_key': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tickets'", 'to': u"orm['snappybouncer.Conversation']"}),
            'created_at': ('snappybouncer.models.AutoNewDateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'support_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'support_nonce': ('django.db.models.fields.CharField', [], {'max_length': '43', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('snappybouncer.models.AutoDateTimeField', [], {'blank': 'True'})
        },
        u'snappybouncer.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'created_at': ('snappybouncer.models.AutoNewDateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('snappybouncer.models.AutoDateTimeField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['snappybouncer']