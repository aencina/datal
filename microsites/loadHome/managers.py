from django.core.urlresolvers import reverse
from core.utils import slugify
from core.search import *
import datetime


class HomeFinder(elastic.ElasticsearchFinder):
    def get_datastream_dictionary(self, doc):

        id = doc['datastream_id']
        title = doc['title']
        slug = slugify(title)
        permalink = reverse('viewDataStream.view', kwargs={'id': id, 'slug': slug})
        created_at = datetime.datetime.fromtimestamp(int(doc['timestamp']))

        return dict(
            id=id,
            title=title,
            category=doc['category_name'],
            created_at=created_at,
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
        created_at = datetime.datetime.fromtimestamp(int(doc['timestamp']))

        return dict(id=dataset_id
                    , title = title
                    , category = doc['category_name']
                    , created_at = created_at
                    , permalink = permalink
                    , type=doc['type'].upper()
                    , account_id = int(doc['account_id'])
                   )

    def get_visualization_dictionary(self, doc):

        id = doc['visualization_id']
        title = doc['title']
        slug = slugify(title)
        permalink = reverse('chart_manager.view', kwargs={'id': id, 'slug': slug})
        created_at = datetime.datetime.fromtimestamp(int(doc['timestamp']))

        return dict(id=id
                    , title = title
                    , category = doc['category_name']
                    , created_at = created_at
                    , permalink = permalink
                    , type=doc['type'].upper()
                    , account_id = int(doc['account_id'])
                   )
