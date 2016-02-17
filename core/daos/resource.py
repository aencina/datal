# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from django.conf import settings


class AbstractDatasetDBDAO():
    """ class for manage access to datasets' database tables """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, language, dataset_id=None, dataset_revision_id=None):
        """ Get full data """
        pass

    @abstractmethod
    def create(self, dataset=None, user=None, collect_type='', impl_details=None, **fields):
        """create a new dataset if needed and a dataset_revision"""
        pass
        
    @abstractmethod
    def update(self, dataset_revision, changed_fields, **fields):
        pass

    @abstractmethod
    def query(self, account_id=None, language=None, page=0, itemsxpage=settings.PAGINATION_RESULTS_PER_PAGE,
              sort_by='-id', filters_dict=None, filter_name=None, exclude=None, filter_status=None,
          filter_category=None, filter_text=None, filter_user=None, full=False):
        pass

    @abstractmethod
    def query_childs(self, dataset_id, language):
        """ Devuelve la jerarquia completa para medir el impacto """
        pass
    
        

class AbstractDataStreamDBDAO():
    """ class for manage access to datastreams' database tables """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, language, datastream_id=None, datastream_revision_id=None):
        """ Get full data """
        pass

    @abstractmethod
    def create(self, datastream=None, user=None, **fields):
        """create a new datastream if needed and a datastream_revision"""
        pass

    @abstractmethod
    def update(self, datastream_revision, changed_fields, **fields):
        pass


    @abstractmethod
    def query(self, account_id=None, language=None, page=0, itemsxpage=settings.PAGINATION_RESULTS_PER_PAGE,
              sort_by='-id', filters_dict=None, filter_name=None, exclude=None, filter_status=None,
          filter_category=None, filter_text=None, filter_user=None, full=False):
        """ Consulta y filtra los datastreams por diversos campos """

        pass

    @abstractmethod
    def query_childs(self, dataset_id, language):
        """ Devuelve la jerarquia completa para medir el impacto """
        pass


class AbstractVisualizationDBDAO():
    """ class for manage access to visualization' database tables """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, language, visualization_id=None, visualization_revision_id=None):
        """ Get full data """
        pass

    @abstractmethod
    def create(self, visualization=None, user=None, collect_type='', impl_details=None, **fields):
        """create a new visualization if needed and a visualization_revision"""
        pass

    @abstractmethod
    def update(self, visualization_revision, changed_fields, **fields):
        pass

    @abstractmethod
    def query(self, account_id=None, language=None, page=0, itemsxpage=settings.PAGINATION_RESULTS_PER_PAGE,
              sort_by='-id', filters_dict=None, filter_name=None, exclude=None, filter_status=None,
          filter_category=None, filter_text=None, filter_user=None, full=False):
        pass

    @abstractmethod
    def query_childs(self, visualization_id, language):
        """ Devuelve la jerarquia completa para medir el impacto """
        pass
