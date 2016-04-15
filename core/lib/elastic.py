# -*- coding: utf-8 -*-
from django.conf import settings
from elasticsearch import Elasticsearch, NotFoundError, RequestError
from core.plugins_point import DatalPluginPoint
import logging


class ElasticsearchIndex():
    """ Gestor para indice elasticsearch"""

    __categories={ "properties" : {
                      "id" : { "type" : "string" },
                      "name" : { "type" : "string",
                                 "fields": {
                                    "lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"},
                                    "category_english_stemmer": {"type":"string", "analyzer": "english"},
                                    "category_spanish_stemmer": {"type":"string", "analyzer": "spanish"}
                                 },
                                 "properties": { 
                                    "category_english": {"type":"string", "analyzer": "english"},
                                    "category_spanish": {"type":"string", "analyzer": "spanish"}
                                 },
 
                      } } }

    
    def __init__(self, url=None):

        # establecemos conexión
        if url:
            print "[WARNING] ignorando config %s, usamos url %s" % (settings.SEARCH_INDEX['url'], url)
            self.es = Elasticsearch(url)
        else:
            self.es = Elasticsearch(settings.SEARCH_INDEX['url'])
 
        es_conf= { "settings": {
                "analysis": {
                  "filter": {
                    "english_stop": {
                      "type":       "stop",
                      "stopwords":  "_english_"
                    },
                    "light_english_stemmer": {
                      "type":       "stemmer",
                      "language":   "light_english"
                    },
                    "english_possessive_stemmer": {
                      "type":       "stemmer",
                      "language":   "english"
                    },
 
                    "light_spanish_stemmer": {
                      "type":       "stemmer",
                      "language":   "light_spanish"
                    },
                    "spanish_possessive_stemmer": {
                      "type":       "stemmer",
                      "language":   "spanish"
                    }
                  },
                    "analyzer": {
                        "case_insensitive_sort": {
                            "tokenizer": "keyword",
                            "filter":  [ "lowercase" ]
                        },
                        "english": {
                          "tokenizer":  "standard",
                          "filter": [
                            "english_possessive_stemmer",
                            "lowercase",
                            "english_stop",
                            "light_english_stemmer",
                            "asciifolding"
                          ]
                        },
                        "spanish": {
                          "tokenizer":  "standard",
                          "filter": [
                            "spanish_possessive_stemmer",
                            "lowercase",
                            "light_spanish_stemmer",
                          ]
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
                  "categories" : self.__categories, # categories

                  "meta_text" : {
                    "properties" : {
                      "field_name" : { "type" : "string" },
                      "field_value" : { "type" : "string"}
                    }
                  }, # meta_text
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
                        "fields": {
                                "text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"},
                                "text_english_stemmer": {"type":"string", "analyzer": "english"},
                                "text_spanish_stemmer": {"type":"string", "analyzer": "spanish"}
                                },
                        "properties": { 
                                "text_english": {"type":"string", "analyzer": "english"},
                                "text_spanish": {"type":"string", "analyzer": "spanish"}
                        },
                      },
                      "created_at" : { "type" : "long" },
                      "modified_at" : { "type" : "long" },
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
                  "categories" : self.__categories, # categories
                  "meta_text" : {
                    "properties" : {
                      "field_name" : { "type" : "string" },
                      "field_value" : { "type" : "string"}
                    }
                  }, # meta_text
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
                        "fields": {
                                "text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"},
                                "text_english_stemmer": {"type":"string", "analyzer": "english"},
                                "text_spanish_stemmer": {"type":"string", "analyzer": "spanish"}
                                },
                        "properties": { 
                                "text_english": {"type":"string", "analyzer": "english"},
                                "text_spanish": {"type":"string", "analyzer": "spanish"}
                        },
                      },
 
                      "created_at" : { "type" : "long" },
                      "modified_at" : { "type" : "long" },
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
                  "categories" : self.__categories, # categories
                  "meta_text" : {
                    "properties" : {
                      "field_name" : { "type" : "string" },
                      "field_value" : { "type" : "string"}
                    }
                  }, # meta_text
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
                        "fields": {
                                "text_lower_sort": {"type":"string", "analyzer": "case_insensitive_sort"},
                                "text_english_stemmer": {"type":"string", "analyzer": "english"},
                                "text_spanish_stemmer": {"type":"string", "analyzer": "spanish"}
                                },
                        "properties": { 
                                "text_english": {"type":"string", "analyzer": "english"},
                                "text_spanish": {"type":"string", "analyzer": "spanish"}
                        },
                      },
 
                      "hits" : { "type" : "integer" },
                      "web_hits" : { "type" : "integer" },
                      "api_hits" : { "type" : "integer" },
                      "created_at" : { "type" : "long" },
                      "modified_at" : { "type" : "long" },
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
            # self.logger.info('Elasticsearch: Agregar al index %s' % str(document))
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

    def search(self, doc_type, query, fields="*" ):
        """Search by query
        :param doc_type:
        :param query:
        :param fields:
        """

        try:
            return self.es.search(index=settings.SEARCH_INDEX['index'], doc_type=doc_type, body=query, _source_include=fields)
        except RequestError,e:
            raise RequestError(e)
        except NotFoundError,e:
            raise NotFoundError,(e)

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

