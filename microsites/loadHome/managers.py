from django.core.urlresolvers import reverse
from core.utils import slugify
from core.search import *
from django.conf import settings
import datetime
import logging
logger = logging.getLogger(__name__)

class HomeFinder(elastic.ElasticsearchFinder):

    def __timestamp(self,timestamp):
        if long(timestamp) < settings.MAX_TIMESTAMP:
            return datetime.datetime.fromtimestamp(int(timestamp)/1000)
            
        return datetime.datetime.now()

    def get_datastream_dictionary(self, doc):

        id = doc['datastream_id']
        title = doc['title']
        slug = slugify(title)
        permalink = reverse('viewDataStream.view', kwargs={'id': id, 'slug': slug})
        created_at = datetime.datetime.fromtimestamp(int(doc['created_at']))
        modified_at= datetime.datetime.fromtimestamp(int(doc['modified_at']))

        return dict(
            id=id,
            title=title,
            category=doc['category_name'],
            created_at=created_at,
            modified_at=modified_at,
            timestamp=self.__timestamp(doc['timestamp']),
            permalink=permalink,
            type=doc['type'].upper(),
            account_id=int(doc['account_id'])
        )

    def get_dataset_dictionary(self, doc):

        dataset_id = doc['dataset_id']
        title = doc['title']
        slug = slugify(title)
        permalink = reverse('manageDatasets.view', urlconf='microsites.urls', kwargs={'dataset_id': dataset_id,
                                                                                               'slug': slug})
        created_at = datetime.datetime.fromtimestamp(int(doc['created_at']))
        modified_at = datetime.datetime.fromtimestamp(int(doc['modified_at']))

        return dict(id=dataset_id
                    , title = title
                    , category = doc['category_name']
                    , created_at = created_at
                    , modified_at=modified_at 
                    , timestamp=self.__timestamp(doc['timestamp'])
                    , permalink = permalink
                    , type=doc['type'].upper()
                    , account_id = int(doc['account_id'])
                   )

    def get_visualization_dictionary(self, doc):

        id = doc['visualization_id']
        title = doc['title']
        slug = slugify(title)
        permalink = reverse('chart_manager.view', kwargs={'id': id, 'slug': slug})
        created_at = datetime.datetime.fromtimestamp(int(doc['created_at']))
        modified_at = datetime.datetime.fromtimestamp(int(doc['modified_at']))

        timestamp=self.__timestamp(doc['timestamp'])

        return dict(id=id
                    , title = title
                    , category = doc['category_name']
                    , created_at = created_at
                    , modified_at = modified_at
                    , timestamp=self.__timestamp(doc['timestamp'])
                    , permalink = permalink
                    , type=doc['type'].upper()
                    , account_id = int(doc['account_id'])
                   )
