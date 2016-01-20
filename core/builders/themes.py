# -*- coding: utf-8 -*-

from core.models import DataStreamRevision, VisualizationRevision, Category
from core.http import add_domains_to_permalinks
from core.daos.datastreams import DataStreamDBDAO
from core.daos.visualizations import VisualizationDBDAO
import json
import logging


class ThemeBuilder(object):
    """docstring for ClassName"""
    def __init__(self, preferences, is_preview, language, account):
        self.preferences = preferences
        self.is_preview = is_preview
        self.language = language
        self.account = account
        self.logger = logging.getLogger(__name__)


    def retrieve_resources_for_slider(self, resourceIds, language):

        datastreamIds = []
        visualizationIds = []
                
        for resource in resourceIds:
            if resource['type']== 'vz':
                visualizationIds.append(resource['id'])
            elif resource['type']== 'ds':
                datastreamIds.append(resource['id'])
                
        data = []

        # usamos el DAO
        for i in datastreamIds:
            try:
                data.append(DataStreamDBDAO().get(language,datastream_id=i, published=True))
            except DataStreamRevision.DoesNotExist:
                self.logger.error("ThemeBuilder.slider: DataStream.id=%s no existe o no esta publicado" % i)

        for i in visualizationIds:
            try:
                data.append(VisualizationDBDAO().get(language,visualization_id=i, published=True))
            except VisualizationRevision.DoesNotExist:
                self.logger.error("ThemeBuilder.slider: Visualization.id=%s no existe o no esta publicado" % i)
 
        return data

    def retrieveResourcePermalinks(self, resourceIds, language):

        datastreamIds = []
        visualizationIds = []
                
        for resource in resourceIds:
            if resource['type']== 'vz':
                visualizationIds.append(resource['id'])
            elif resource['type']== 'ds':
                datastreamIds.append(resource['id'])
                
        resources = []
        if datastreamIds:
            idsDataStream = ','.join(datastreamIds)
            resources =  DataStreamDBDAO().query_hot_n(10,language, hot = idsDataStream)
                
        if visualizationIds:
            idsVisualization = ','.join(visualizationIds)
            resources +=  VisualizationDBDAO().query_hot_n(language, hot = idsVisualization)

     
        add_domains_to_permalinks(resources)

        return resources

    def parse(self):
        response = {
            'preferences': self.preferences,
            'account': self.account,
            'is_preview': self.is_preview,
            'language': self.language,
            'config': {},
            'datastreams': [],
            'resources': [],
            'categories': [],
            'account_id': self.account.id,
            'template_path': None
        }

        jsonObject = None
        if self.is_preview:
            jsonObject = json.loads(self.preferences["account_preview"], strict=False)
        elif self.preferences["account_has_home"]:
            jsonObject = json.loads(self.preferences["account_home"], strict=False)


        if jsonObject:
            response['config'] = config = jsonObject['config']
            response['template_path'] = 'loadHome/home_'+jsonObject['theme']+'.html'

            if config:
                if 'sliderSection' in config:
                    response['resources_slider'] = self.retrieve_resources_for_slider(
                        config['sliderSection'], self.language)
                if 'linkSection' in config:
                    response['resources'] = self.retrieveResourcePermalinks(
                        config['linkSection'], self.language)

            #devuelve los ID de las cuentas federadas
            response['federated_accounts_ids']=[x['id'] for x in self.account.account_set.values('id').all()]

            if response['federated_accounts_ids']: # si hay IDS, es que es una cuenta federada
                federated_accounts=[]
                for pk in response['federated_accounts_ids']:
                    domain = Account.objects.get(id=pk).get_preference('account.domain')
                    name = Account.objects.get(id=pk).get_preference('account.name')
                    federated_accounts.append({"id": pk, "domain": domain, "link": domain, "name": name})
                response['federated_accounts'] = federated_accounts
                response['categories'] = Category.objects.get_for_home(self.language, response['federated_accounts_ids']+[response['account_id']])
            else:
                response['categories'] = Category.objects.get_for_home(self.language, response['account_id'])

            return response
