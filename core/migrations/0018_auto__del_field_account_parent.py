# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Account.parent'
        db.delete_column('ao_accounts', 'parent_id')

        # Adding M2M table for field parent on 'Account'
        m2m_table_name = db.shorten_name('ao_accounts_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_account', models.ForeignKey(orm[u'core.account'], null=False)),
            ('to_account', models.ForeignKey(orm[u'core.account'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_account_id', 'to_account_id'])


    def backwards(self, orm):
        # Adding field 'Account.parent'
        db.add_column('ao_accounts', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Account'], null=True, on_delete=models.PROTECT, blank=True),
                      keep_default=False)

        # Removing M2M table for field parent on 'Account'
        db.delete_table(db.shorten_name('ao_accounts_parent'))


    models = {
        u'core.account': {
            'Meta': {'object_name': 'Account', 'db_table': "'ao_accounts'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AccountLevel']"}),
            'meta_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Account']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '4'})
        },
        u'core.accountlevel': {
            'Meta': {'object_name': 'AccountLevel', 'db_table': "'ao_account_levels'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.application': {
            'Meta': {'object_name': 'Application', 'db_table': "'ao_applications'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']", 'null': 'True', 'blank': 'True'}),
            'auth_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'domains': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'public_auth_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'core.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'ao_categories'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.categoryi18n': {
            'Meta': {'object_name': 'CategoryI18n', 'db_table': "'ao_categories_i18n'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30'})
        },
        u'core.dataset': {
            'Meta': {'object_name': 'Dataset', 'db_table': "'ao_datasets'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '29'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dead': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'last_published_revision': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_published_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.DatasetRevision']"}),
            'last_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.DatasetRevision']"}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'})
        },
        u'core.dataseti18n': {
            'Meta': {'object_name': 'DatasetI18n', 'db_table': "'ao_dataset_i18n'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DatasetRevision']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'core.datasetrevision': {
            'Meta': {'ordering': "['-id']", 'object_name': 'DatasetRevision', 'db_table': "'ao_dataset_revisions'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Dataset']"}),
            'end_point': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'frequency': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'impl_type': ('django.db.models.fields.IntegerField', [], {}),
            'license_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mbox': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spatial': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'})
        },
        u'core.datastream': {
            'Meta': {'object_name': 'DataStream', 'db_table': "'ao_datastreams'"},
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '29'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_published_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_published_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.DataStreamRevision']"}),
            'last_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.DataStreamRevision']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'})
        },
        u'core.datastreamcomment': {
            'Meta': {'object_name': 'DataStreamComment', 'db_table': "'ao_datastream_comments'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"})
        },
        u'core.datastreamhits': {
            'Meta': {'object_name': 'DataStreamHits', 'db_table': "'ao_datastream_hits'"},
            'channel_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.datastreami18n': {
            'Meta': {'object_name': 'DatastreamI18n', 'db_table': "'ao_datastream_i18n'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStreamRevision']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'core.datastreamparameter': {
            'Meta': {'ordering': "['position']", 'unique_together': "(('datastream_revision', 'name'),)", 'object_name': 'DataStreamParameter', 'db_table': "'ao_datastream_parameters'"},
            'datastream_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStreamRevision']", 'null': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'core.datastreamrank': {
            'Meta': {'object_name': 'DataStreamRank', 'db_table': "'ao_datastream_ranks'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'core.datastreamrevision': {
            'Meta': {'ordering': "['-id']", 'object_name': 'DataStreamRevision', 'db_table': "'ao_datastream_revisions'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_source': ('django.db.models.fields.TextField', [], {}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Dataset']"}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rdf_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'select_statement': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'})
        },
        u'core.grant': {
            'Meta': {'object_name': 'Grant', 'db_table': "'ao_user_grants'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Guest']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'privilege': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Privilege']", 'null': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Role']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'on_delete': 'models.PROTECT'})
        },
        u'core.guest': {
            'Meta': {'object_name': 'Guest', 'db_table': "'ao_user_guests'"},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'grants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Privilege']", 'through': u"orm['core.Grant']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.log': {
            'Meta': {'object_name': 'Log', 'db_table': "'ao_logs'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']", 'null': 'True', 'on_delete': 'models.DO_NOTHING'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.DO_NOTHING'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Visualization']", 'null': 'True', 'on_delete': 'models.DO_NOTHING'})
        },
        u'core.objectgrant': {
            'Meta': {'object_name': 'ObjectGrant', 'db_table': "'ao_user_object_grants'"},
            'auth_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']", 'null': 'True'}),
            'grant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Grant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Visualization']", 'null': 'True'})
        },
        u'core.preference': {
            'Meta': {'object_name': 'Preference', 'db_table': "'ao_account_preferences'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'core.privilege': {
            'Meta': {'object_name': 'Privilege', 'db_table': "'ao_user_privileges'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'core.role': {
            'Meta': {'object_name': 'Role', 'db_table': "'ao_user_roles'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'grants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Privilege']", 'through': u"orm['core.Grant']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'core.setting': {
            'Meta': {'object_name': 'Setting', 'db_table': "'ao_settings'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'core.source': {
            'Meta': {'object_name': 'Source', 'db_table': "'ao_sources'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        u'core.sourcedataset': {
            'Meta': {'object_name': 'SourceDataset', 'db_table': "'ao_sources_dataset_revision'"},
            'datasetrevision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DatasetRevision']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']", 'null': 'True'})
        },
        u'core.sourcedatastream': {
            'Meta': {'object_name': 'SourceDatastream', 'db_table': "'ao_sources_datastream_revision'"},
            'datastreamrevision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStreamRevision']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']", 'null': 'True'})
        },
        u'core.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'ao_tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'core.tagdataset': {
            'Meta': {'object_name': 'TagDataset', 'db_table': "'ao_tags_dataset'"},
            'datasetrevision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DatasetRevision']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tag']", 'null': 'True'})
        },
        u'core.tagdatastream': {
            'Meta': {'object_name': 'TagDatastream', 'db_table': "'ao_tags_datastream'"},
            'datastreamrevision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStreamRevision']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tag']", 'null': 'True'})
        },
        u'core.tagvisualization': {
            'Meta': {'object_name': 'TagVisualization', 'db_table': "'ao_tags_visualization'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Tag']", 'null': 'True'}),
            'visualizationrevision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.VisualizationRevision']", 'null': 'True'})
        },
        u'core.threshold': {
            'Meta': {'object_name': 'Threshold', 'db_table': "'ao_account_thresholds'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']", 'null': 'True', 'blank': 'True'}),
            'account_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AccountLevel']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User', 'db_table': "'ao_users'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '3', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'grants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Privilege']", 'through': u"orm['core.Grant']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nick': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'ocupation': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '155'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Role']", 'db_table': "'ao_user_role_roles'", 'symmetrical': 'False'})
        },
        u'core.userpasstickets': {
            'Meta': {'object_name': 'UserPassTickets', 'db_table': "'ao_user_passtickets'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '38'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '38'})
        },
        u'core.visualization': {
            'Meta': {'object_name': 'Visualization', 'db_table': "'ao_visualizations'"},
            'datastream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStream']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '29'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_published_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_published_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.VisualizationRevision']"}),
            'last_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_revision'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.VisualizationRevision']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'})
        },
        u'core.visualizationhits': {
            'Meta': {'object_name': 'VisualizationHits', 'db_table': "'ao_visualization_hits'"},
            'channel_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Visualization']"})
        },
        u'core.visualizationi18n': {
            'Meta': {'object_name': 'VisualizationI18n', 'db_table': "'ao_visualizations_i18n'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'visualization_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.VisualizationRevision']"})
        },
        u'core.visualizationrevision': {
            'Meta': {'ordering': "['-id']", 'object_name': 'VisualizationRevision', 'db_table': "'ao_visualizations_revisions'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastream_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DataStreamRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lib': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'meta_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'on_delete': 'models.PROTECT'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Visualization']"})
        }
    }

    complete_apps = ['core']