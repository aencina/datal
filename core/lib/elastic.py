# -*- coding: utf-8 -*-
from django.conf import settings
from elasticsearch import Elasticsearch, NotFoundError, RequestError
from core.plugins_point import DatalPluginPoint
import logging


class ElasticsearchIndex():
    """ Gestor para indice elasticsearch"""
    
    def __init__(self):

        # establecemos conexión
        self.es = Elasticsearch(settings.SEARCH_INDEX['url'])

        es_conf= { "settings": {
                "analysis": {
                    "analyzer": {
                        "case_insensitive_sort": {
                            "tokenizer": "keyword",
                            "filter":  [ "lowercase" ]
                        }
                    }
                }               
            } }

        # se crea el indice si es que no existe
        # Ignora que exista el indice
        indices = self.es.indices.create(index=settings.SEARCH_INDEX['index'], body=es_conf, ignore=400)

        # primera vez que empuja el index
        try:
            if indices['acknowledged']:
                for doc_type in ["ds","dt","vz"]:
                    self.es.indices.put_mapping(index=settings.SEARCH_INDEX['index'], doc_type=doc_type, body=self.__get_mapping(doc_type))
                for finder in DatalPluginPoint.get_active_with_att('finder'):
                    self.es.indices.put_mapping(index=settings.SEARCH_INDEX['index'], doc_type=finder.doc_type, body=self.__get_mapping(finder.doc_type))
        # Ya existe un index
        except KeyError:
            pass

        self.logger = logging.getLogger(__name__)

    def __get_mapping(self, doc_type):
        if doc_type == "ds":
            return self.__get_datastream_mapping()
        elif doc_type == "dt":
            return self.__get_dataset_mapping()
        elif doc_type == "vz":
            return self.__get_visualization_mapping()

        for finder in DatalPluginPoint.get_active_with_att('finder'):
            if finder.doc_type == doc_type:
                return finder.get_mapping()

    def __get_datastream_mapping(self):
        return {"ds" : {
                "properties" : {
                  "categories" : {
                    "properties" : {
                      "id" : { "type" : "string" },
                      "name" : { "type" : "string", 
                                 "index" : "not_analyzed" }
                    }
                  }, # categories
                  "docid" : { "type" : "string" },
                  "fields" : {
                    "properties" : {
                      "account_id" : { "type" : "long" },
                      "datastream__revision_id" : { "type" : "long" },
                      "datastream_id" : { "type" : "long" },
                      "resource_id" : { "type" : "long" },
                      "revision_id" : { "type" : "long" },
                      "description" : { "type" : "string" },
                      "end_point" : { "type" : "string" },
                      "owner_nick" : { "type" : "string" },
                      "parameters" : { "type" : "string" },
                      "tags" : { "type" : "string" },
                      "text" : {
                        "type" : "string",
                        "fields": {"text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                      },
                      "timestamp" : { "type" : "long" },
                      "hits" : { "type" : "integer" },
                      "web_hits" : { "type" : "integer" },
                      "api_hits" : { "type" : "integer" },
                      "title" : { "type" : "string" ,
                        "fields": {"title_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                          },
                      "type" : { "type" : "string" }
                    }
                  } # fields
                }
              }
        }

    def __get_dataset_mapping(self):
        return {"dt" : {
                "properties" : {
                  "categories" : {
                    "properties" : {
                      "id" : { "type" : "string" },
                      "name" : { "type" : "string",
                                 "index" : "not_analyzed" }
                    }
                  }, # categories
                  "docid" : { "type" : "string" },
                  "fields" : {
                    "properties" : {
                      "account_id" : { "type" : "long" },
                      "datasetrevision_id" : { "type" : "long" },
                      "dataset_id" : { "type" : "long" },
                      "resource_id" : { "type" : "long" },
                      "revision_id" : { "type" : "long" },
                      "description" : { "type" : "string" },
                      "end_point" : { "type" : "string" },
                      "owner_nick" : { "type" : "string" },
                      "parameters" : { "type" : "string" },
                      "tags" : { "type" : "string" },
                      "text" : {
                        "type" : "string",
                        "fields": {"text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                      },
                      "timestamp" : { "type" : "long" },
                      "hits" : { "type" : "integer" },
                      "web_hits" : { "type" : "integer" },
                      "api_hits" : { "type" : "integer" },
                      "title" : { "type" : "string" ,
                        "fields": {"title_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                          },
                      "type" : { "type" : "string" }
                    }
                  } # fields
                }
              }
        }
 
    def __get_visualization_mapping(self):
        return {"vz" : {
                "properties" : {
                  "categories" : {
                    "properties" : {
                      "id" : { "type" : "string" },
                      "name" : { "type" : "string",
                                 "index" : "not_analyzed" }
                    }
                  }, # categories
                  "docid" : { "type" : "string" },
                  "fields" : {
                    "properties" : {
                      "account_id" : { "type" : "long" },
                      "resource_id" : { "type" : "long" },
                      "revision_id" : { "type" : "long" },
                      "visualization_revision_id" : { "type" : "long" },
                      "visualization_id" : { "type" : "long" },
                      "description" : { "type" : "string" },
                      "end_point" : { "type" : "string" },
                      "owner_nick" : { "type" : "string" },
                      "parameters" : { "type" : "string" },
                      "tags" : { "type" : "string" },
                      "text" : {
                        "type" : "string",
                        "fields": {"text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                      },
                      "hits" : { "type" : "integer" },
                      "web_hits" : { "type" : "integer" },
                      "api_hits" : { "type" : "integer" },
                      "timestamp" : { "type" : "long" },
                      "title" : { "type" : "string" ,
                        "fields": {"title_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"}}
                          },
                      "type" : { "type" : "string" }
                    }
                  } # fields
                }
              }
        }

    def indexit(self, document):
        """add document to index
        :param document:
        """

        if document:
            self.logger.info('Elasticsearch: Agregar al index %s' % str(document))
            try:
                return self.es.create(
                    index=settings.SEARCH_INDEX['index'],
                    body=document,
                    doc_type=document['fields']['type'],
                    id=document['docid'])
            except:
                return self.es.index(
                    index=settings.SEARCH_INDEX['index'],
                    body=document,
                    doc_type=document['fields']['type'],
                    id=document['docid'])


        logger.error(u"Elasticsearch: Ningún documento para indexar")
        return False
        
    def count(self, doc_type=None):
        """return %d of documents in index, doc_type (opt) filter this document type"""

        if doc_type:
            return self.es.count(index=settings.SEARCH_INDEX['index'], doc_type=doc_type)['count']
        else:
            return self.es.count(index=settings.SEARCH_INDEX['index'])['count']
        
    def delete_document(self, document):
        """delete by ID"""

        try:
            output = self.es.delete(index=settings.SEARCH_INDEX['index'], id=document['docid'], doc_type=document['type'])
            return output
        except NotFoundError:
            self.logger.error("ERROR NotFound: ID %s not found in index" % document['docid'])
            return {u'found': False, u'documment': document, u'index': settings.SEARCH_INDEX['index']}
        except KeyError:
            self.logger.error("ERROR KeyError: Document error (doc: %s)" % str(document))
        except TypeError:
            self.logger.error("ERROR TypeError: Document error (doc: %s)" % str(document))

        return False

    def __filterDeleted(self, item):
        return item['found']

    def __filterNotDeleted(self, item):
        return not item['found']

    def flush_index(self):
        return self.es.indices.delete(index=settings.SEARCH_INDEX['index'], ignore=[400, 404])

    def delete_documents(self, documents):
        """Delete from a list. Return [list(deleted), list(notdeleted)]
        :param documents:
        """
        result = map(self.delete_document, documents)

        documents_deleted=filter(self.__filterDeleted,result)
        documents_not_deleted=filter(self.__filterNotDeleted,result)

        return [documents_deleted, documents_not_deleted]

    def update(self, document):
        """ Update by id
        :param document:
        """
        # Me lo pediste vos nacho, despues no me putees
        # te tengo que putear, seas quien seas
        #return True
        try:
            return self.es.update(index=settings.SEARCH_INDEX['index'], id=document['docid'], doc_type=document['type'], body=document)
        except RequestError,e:
            raise RequestError(e)
        except NotFoundError,e:
            raise NotFoundError,(e)

