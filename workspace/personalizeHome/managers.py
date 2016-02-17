from core.search import *

class ThemeFinder(elastic.ElasticsearchFinder):

#    def __init__(self):
#        elastic.ElasticsearchFinder.__init__(self)

    def get_datastream_dictionary(self, doc):
        return dict(id=doc['datastream_id'], label=doc['title'], value=doc['title'], type=doc['type'])

    def get_dataset_dictionary(self, doc):
        return dict(id=doc['dataset_id'], label=doc['title'], value=doc['title'], type=doc['type'])

    def get_visualization_dictionary(self, doc):
        return dict(id=doc['visualization_id'], label=doc['title'], value=doc['title'], type=doc['type'])
        