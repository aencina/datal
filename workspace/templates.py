# -*- coding: utf-8 -*-
"""
Templates for errors
"""

from core.templates import *
import json

class DefaultDataViewEdit(Template):

    def __init__(self, template="datastream_edit_response.json"):
        tmpl = "{%% include '%s' %%}" % template
        super(DefaultDataViewEdit, self).__init__(tmpl)

    def render(self, categories, status, allowed_status, datastream_revision, datastreami18n, dao):
        ctx = Context({
            "categories": categories,
            "status": status,
            "allowed_status": allowed_status,
            "datastream_revision": datastream_revision,
            'datastreami18n': datastreami18n,
            'dao': dao,
        })
        return super(DefaultDataViewEdit, self).render(ctx)


class DatasetList(Template):

    def __init__(self, template="manageDatasets/dataset_list.json"):
        tmpl = "{%% include '%s' %%}" % template
        super(DatasetList, self).__init__(tmpl)

    def render(self, data):
        ctx = Context({"data": data})
        return super(DatasetList, self).render(ctx)

class DatastreamList(Template):

    def __init__(self, template="manageDataviews/datastream_list.json"):
        tmpl = "{%% include '%s' %%}" % template
        super(DatastreamList, self).__init__(tmpl)

    def render(self, data):
        ctx = Context({"data": data})
        return super(DatastreamList, self).render(ctx)